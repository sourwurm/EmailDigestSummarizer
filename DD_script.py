#!/usr/bin/env python
# coding: utf-8

# # Medium Daily Digest Summarizer
# 
# Gets all of your daily digest emails from medium and summarizing each article within them! Have all of your articles summarized while you fix youself a cup of coffee :^)

# In[1]:


import imaplib
import email
from newspaper import Article, ArticleException, news_pool

import pandas as pd
import numpy as np

from nltk import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import re
import heapq

from datetime import date


# ### Scraping emails

# In[2]:


#user should be your email address in the form "----@gmail.com"
user = 'YOUR EMAIL'

#password is ideally an app password to maintain account security
#instructions on how to get your gmail app password: https://support.google.com/accounts/answer/185833?hl=en
password = 'YOUR PASSWORD'

#imap url for gmail
imap_url = 'imap.gmail.com'


# In[3]:


def get_body(msg):
    
    
    #if nested, apply function until you get to the content
    if msg.is_multipart():
        return get_body(msg.get_payload(0))
    
    #return content
    else:
        return msg.get_payload(None, True)


# In[4]:


def search(key, value, con):
    
    #search for key value pairs matching FROM noreply@medium.com
    result, data = con.search(None, key, '"{}"'.format(value))
    
    return data


# In[5]:


def get_emails(result_bytes):
    
    #get emails under a particular label
    #in this case, the inbox
    #stored inside a list
    msgs = []
    
    ####only retrieving the latest email
    num = result_bytes[0].split()[-1]

    typ, data = con.fetch(num, '(RFC822)')
    msgs.append(data)
    
    ####if youd like to retrieve all emails, uncomment the following:
    
    #for num in result_bytes[0].split():
        #typ, data = con.fetch(num, '(RFC822)')
        #msgs.append(data)
    
    return msgs


# In[6]:


#logging in with credentials and accessing emails in the inbox
#note: this will include ALL emails in the inbox, not just those seen in the section labeled "Primary"
#(you might have more emails in your inbox than you think)
con = imaplib.IMAP4_SSL(imap_url, 993)
con.login(user, password)
con.select('Inbox')


# In[7]:


#getting emails from medium
msgs =  get_emails(search('FROM', 'noreply@medium.com', con))


# In[8]:


#extracting information contained between parentheses
#aka article links
p1 = []
for msg in msgs[::-1]:
    for sent in msg:
        p1.append(re.findall('\(([^)]+)', str(sent)))


# ### Getting article links

# In[9]:


#filtering out unwanted links
check = []

for lst in p1:
    
    for string in lst:
        match_lst = re.findall('.*(?:\/.*){4}', str(string))
        
        for val in match_lst:
            
            if (len(val) > 1) and ('https://medium.com/' in val):
                check.append(val)


# In[10]:


links = []

for val in check:
     
    #remove everything after '?'
    #remove '=\\r\\n' from links       
    val = val.replace ('=\\r\\n', '')
    val = re.sub('[?].*','', val)
    
    #removing special cases
    if (len(val) > 45) and ('E2=80=A6' not in val) and ('api/requests/' not in val):
    
        #link stored in a new list
        links.append(val)


# ### Scraping articles

# In[11]:


title = []
author = []
published = []
body = []

#downloading articles
#multi-threading to be nicer to medium
articles = [Article(link, fetch_images = False) for link in links]
news_pool.set(articles, threads_per_source = 6)
news_pool.join()

#getting title, author, publish date, and text body for each article
for i in range(0, len(articles)):
    
    try:
        articles[i].parse()
    
    except ArticleException:
        pass
    
    #appending each to the corresponding list
    title.append(articles[i].title)
    author.append(articles[i].authors)
    published.append(articles[i].publish_date)
    body.append(articles[i].text)


# In[12]:


#putting together the dataframe
df = pd.DataFrame({'Link': links, 'Author':author, 'Title':title, 'Published':published, 'Body':body})


# ### Cleaning text

# In[13]:


def body_wash(string, punct = False):
    
    #removing line breaks, digits, and empty space
    string = string.replace('\n\n', ' ')
    string = re.sub(r'\[[0-9]*\]', ' ', string)
    string = re.sub(r'\s+', ' ', string)
    
    if punct:
        
        #removes punctuation
        string = re.sub(r'[^a-zA-Z]', ' ', string)
        
        return string
    
    else:

        return string


# In[14]:


#cleaning the body of test
df['Body'] = df['Body'].apply(body_wash)


# In[15]:


sent_lst = []

#each article represented as lists of its sentences
for body in df['Body']:
    sent_lst.append(sent_tokenize(body))


# In[16]:


#body of text cleaned, with puntuation removed
formatted = list(df['Body'].apply(body_wash, punct = True))


# ### Summarizing articles

# In[17]:


stop = stopwords.words('english')

freqs = []

#getting word frequencies for each article
for txt in formatted:
    
    #every article will get its own dictionary, containing the articles word frequencies
    word_freq = {}
    
    for word in word_tokenize(txt):
        
        if word not in stop:
            
            #adds word to the dictionary if doesnt already exists
            if word not in word_freq.keys():
                word_freq[word] = 1
                
            #otherwise just adds it to the existing count
            else:
                word_freq[word] += 1
                
    #adding each dictionary to the list           
    freqs.append(word_freq)


# In[18]:


#getting the relative frequency of each word
for word_freq in freqs:
    
    #max word frequency
    max_freq = max(word_freq.values())

    for word in word_freq.keys():
        
        #dividing each word frequency by the max frequency
        word_freq[word] = (word_freq[word]/max_freq)


# In[19]:


scores = []

#getting each sentences score, according to its word frequencies
for i, lst in enumerate(sent_lst):
    
    sent_scores = {}
    
    #looping through every sentence in the article
    for sent in lst:
        
        #looping through every word in the sentence
        for word in word_tokenize(sent.lower()):
            
            #if the word is a key in the word frequency dictionary corresponding to its article
            if word in freqs[i].keys():
                
                #less than 30 words in the sentence
                if len(sent.split(' ')) < 30:
                    
                    #if the sentence isnt already scored
                    if sent not in sent_scores.keys():
                        sent_scores[sent] = freqs[i][word]
                    
                    #if its already there, add the value
                    else:
                        sent_scores[sent] += freqs[i][word]
                        
    scores.append(sent_scores)
                    
                    


# In[20]:


#empty list holding every summary
sums = []

#looping through each article
for sent_score in scores:
    
    #getting the 7 highest scoring sentences for each article
    summary_sent = heapq.nlargest(7, sent_score, key = sent_score.get)
    
    #joining each summary into a single string
    summary = ' '.join(summary_sent)
    
    #appending the summary
    sums.append(summary)


# In[21]:


df['Summary'] = sums


# #### Full Article

# In[28]:


df.iloc[5,2]


# In[22]:


df.iloc[5,4]


# #### Summarized Article

# In[23]:


df.iloc[5,5]


# In[24]:


df


# ### Saving to a csv

# In[25]:


#including todays date
today = date.today().strftime("%b-%d-%Y")


# In[26]:


#DD: Daily Digest
df.to_csv('DD_'+ today +'.csv')


# In[ ]:





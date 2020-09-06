# Email Digest Summarizer

Every other day or so I get an Email from Medium.com with a daily digest of articles they think I might like.
This a cool feature and I like to go through the articles with a cup of coffee when I have the time. The only problem is
that Medium articles are prone to click-bait titles, lengthy rambling, and sometimes even false information. 
Usually I have to sift through the articles, skimming to see if I can spot anything worth reading, and by that point my coffee might be cold :/

Here I aim to optimize this sifting process by summarizing every article instead!

## Note
This script looks for Medium emails in your Inbox; meaning it's looking in Primary, Social, Promotions, etc.. This can potentially be A LOT of articles if you're not
on top of deleting your emails. To control this, the script only returns the most recent email by default. 

If you'd like to retrieve ALL emails from medium, then uncomment the code I left under the get_emails function. This is not recommended as each email may contain up to 20 articles, and if you have say 20 daily digests in your inbox, you might have more than you care to read and can expect the script to take much longer to run.

## Getting Started
- Run pip install -r requirements.txt to install all dependencies.
- Download punctuation lexicon: import nltk -> nltk.download('punkt')
- Download stopwords lexicon: import nltk -> nltk.download('stopwords')

Open either the notebook or .py file and enter your email and password to your gmail account. I highly recommend you create an app password with gmail in order to ensure your account remains secure! Here's a how-to for gmail users: https://support.google.com/accounts/answer/185833?hl=en

After that, just run the script and your articles should appear in your browser window. The links in the navigator bar take you to your accounts on the respective sites, for ease of getting your day started. The links at the very bottom under "Contact" link to my own profiles, in case you're curious to learn more about me :)

#### Home Screen

![](/ex2.png)

#### Example Summary

![](/ex1.png)

Note: Articles with missing authors no longer display empty brackets.

## Breakdown of Steps
This is a high-level explanation of the steps the script takes.
1. Sign in to gmail
2. Look for emails coming from noreply@Medium.com
3. Parse those emails for the article links
4. Scrape articles from Medium
5. Split each article into its sentences
6. Calculate weighted word frequencies for every word in every sentence, for every article
7. Score each sentence in every article based on the sum of its weighted word frequencies
8. Get the seven highest-ranking sentences to create a summary of the article
9. Convert relevant info into HTML
10. Create a temporary HTML file, and present it

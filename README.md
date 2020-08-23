# Email Digest Summarizer

Every other day or so I get an Email from Medium.com with a daily digest of articles they think I might like.
This a cool feature and I like to go through the articles with a cup of coffee when I have the time. The only problem is
that Medium articles are prone to click-bait titles that don't necessarily represent what the article is actully about.
Usually I have to sift through the articles, skimming to see if I can glance anything worth reading, and by that point: my coffee might be cold :/

## The Script

This script will access your Medium Daily Digest emails and return a csv file containing 7-sentence summaries of every article linked in the digest 
(along with author, title, and a link to the article of course). This summarization aims to provide a quick "tl;dr" for when you think an articles title
*seems* promising, but you just wanna make sure. Additionally, the csv format opens some cool doors in case anyone is curious to run some NLP on any of their
recommended articles.

Currently experimenting with sending the summaries directly to your email as well, so stay tuned!

## Getting Started

Open either the notebook or .py file and enter your email and password to your gmail account. I highly recommend you create an app password with gmail in order to ensure your
account remains secure! Here's a how-to by Google: https://support.google.com/accounts/answer/185833?hl=en

After that, just run the script and you're good to go. The csv will appear in the same folder that you're running the script from.


## Breakdown of Steps

1. Signs in to gmail
2. Look for emails coming from noreply@Medium.com
3. Parse those emails for the article links
4. Scrape article from medium
5. Split each article into its sentences
6. Calculate weighted word frequencies for every word in every sentence, for every article
7. Score each sentence in every article based on the sum of its weighted word frequencies
8. Get the seven highest-ranking sentences to create a summary of the article
9. Export to csv

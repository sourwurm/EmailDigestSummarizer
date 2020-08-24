# Email Digest Summarizer

Every other day or so I get an Email from Medium.com with a daily digest of articles they think I might like.
This a cool feature and I like to go through the articles with a cup of coffee when I have the time. The only problem is
that Medium articles are prone to click-bait titles that don't necessarily represent what the article is actully about.
Usually I have to sift through the articles, skimming to see if I can spot anything worth reading, and by that point my coffee might be cold :/

Here I aim to optimize this sifting process by summarizing every article instead!

## Getting Started
This script looks for Medium emails in your Inbox; meaning it's looking in Primary, Social, Promotions, etc.. This can potentially be A LOT of articles if you're not
on top of deleting your emails. To control this, the script only returns the most recent email by default. 

If you'd like to retrieve ALL emails from medium, then uncomment the code I left under the get_emails function. This is generally unrecommended as each email may contain up to 20 articles, and if you have say 20 daily digests lying around in your inbox, you might have more than you care to read and can expect the script to take much longer to run.

Otherwise, open either the notebook or .py file and enter your email and password to your gmail account. I highly recommend you create an app password with gmail in order to ensure your account remains secure! Here's a how-to for gmail users: https://support.google.com/accounts/answer/185833?hl=en

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


### Next Steps for this Project
Working on presenting your summarized articles in a web-browser format. So after the script finishes running, a browser window opens, containing the summaries for every article, along with their corresponding info (title, author, link, etc.).

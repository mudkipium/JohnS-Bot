import praw
import pdb
import re
import os

reddit = praw.Reddit('johnSbot')
subreddit = reddit.subreddit('all')

if not os.path.isfile('replied_posts.txt'):
    replied_posts = []
else:
    with open('replied_posts.txt', 'r') as f:
        replied_posts = f.read()
        replied_posts = replied_posts.split("\n")
        replied_posts = list(filter(None, replied_posts))

for submission in subreddit.new(limit=5):
    if submission.id not in replied_posts:
        if re.search('john hopkins', submission.title, re.IGNORECASE):
            submission.reply('*Johns Hopkins')
            replied_posts.append(submission.id)

with open('replied_posts.txt', 'w') as f:
    for post_id in replied_posts:
        f.write(post_id + '\n')
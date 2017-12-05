import praw
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

for submission in subreddit.stream.submissions():
    if submission.id not in replied_posts:
        if re.search(r'\bjohn hopkins\b', submission.title, re.IGNORECASE):
            submission.reply('*Johns Hopkins\n\n---\n\n^I ^am ^a ^bot!')
            replied_posts.append(submission.id)
	    print('Replying to: ', submission.title)
        if re.search(r'\bjohn hopkin\b', submission.title, re.IGNORECASE):
            submission.reply('*Johns Hopkin\n\n---\n\n^I ^am ^a ^bot!')
            replied_posts.append(submission.id)
	    print('Replying to: ', submission.title)

with open('replied_posts.txt', 'w') as f:
    for post_id in replied_posts:
        f.write(post_id + '\n')

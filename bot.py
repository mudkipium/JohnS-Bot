import os
import praw
import re
import time

from praw.models.util import stream_generator
from praw.models.reddit.comment import Comment
from praw.models.reddit.submission import Submission

signature = '\n\n---\n\n^I ^am ^a ^bot, ^proud ^defender ^of ^the ^[S](https://www.jhu.edu).'

reddit = praw.Reddit('johnSbot')
subreddit = reddit.subreddit('all')


def submissions_and_comments(sub, **kwargs):
    results = []
    results.extend(sub.new(**kwargs))
    results.extend(sub.comments(**kwargs))
    results.sort(key=lambda post: post.created_utc, reverse=True)
    return results

stream = stream_generator(lambda **kwargs: submissions_and_comments(subreddit, **kwargs))

if not os.path.isfile('replied_posts.txt'):
    replied_posts = []
else:
    with open('replied_posts.txt', 'r') as f:
        replied_posts = f.read()
        replied_posts = replied_posts.split("\n")
        replied_posts = list(filter(None, replied_posts))

if not os.path.isfile('replied_comments.txt'):
    replied_comments = []
else:
    with open('replied_comments.txt', 'r') as f:
        replied_comments = f.read()
        replied_comments = replied_comments.split("\n")
        replied_comments = list(filter(None, replied_comments))

while True:
    try:
        for post in stream:
            if isinstance(post, Submission):
                if post.id not in replied_posts:
                    if (re.search(r'\bjohn hopkins\b', post.title, re.IGNORECASE) or
                        re.search(r'\bjohn hopkins\b', post.selftext, re.IGNORECASE)):
                        post.reply('*Johns Hopkins' + signature)
                        replied_posts.append(post.id)
                        print('Replying to: ', post.title)
                    elif (re.search(r'\bjohn hopkin\b', post.title, re.IGNORECASE) or
                        re.search(r'\bjohn hopkin\b', post.selftext, re.IGNORECASE)):
                        post.reply('*Johns Hopkin' + signature)
                        replied_posts.append(post.id)
                        print('Replying to: ', post.title)
            elif isinstance(post, Comment):
                if post.id not in replied_comments:
                    if (re.search(r'\bjohn hopkins\b', post.body, re.IGNORECASE)):
                        post.reply('*Johns Hopkins' + signature)
                        replied_comments.append(post.id)
                        print('Replying to: ', post.body)
                    elif (re.search(r'\bjohn hopkin\b', post.body, re.IGNORECASE)):
                        post.reply('*Johns Hopkin' + signature)
                        replied_comments.append(post.id)
                        print('Replying to: ', post.body)
    except KeyboardInterrupt:
        print('KeyboardInterrupt')
        break
    except Exception as e:
        print('Exception:', e)
        time.sleep(60)

with open('replied_posts.txt', 'w') as f:
    for post_id in replied_posts:
        f.write(post_id + '\n')

with open('replied_comments.txt', 'w') as f:
    for post_id in replied_comments:
        f.write(post_id + '\n')

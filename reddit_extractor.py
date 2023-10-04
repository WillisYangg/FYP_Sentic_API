import praw
import pandas as pd
import sys

user_agent = "Scrapper 1.0 by /u/willissssa"
client_id = "7yQTXog0_Zi1dAWu0WkMkg"
client_secret="__whBicqP2M30uNn1u-lvqfNUUap1Q"

def reddit_api():
    global reddit
    reddit = praw.Reddit(
        client_id = client_id,
        client_secret = client_secret,
        user_agent = user_agent
    )
    
def reddit_data_extraction(reddit_page):
    posts=[]
    reddit_posts = reddit.subreddit("'"+reddit_page+"'")
    for post in reddit_posts.hot(limit=None):
        posts.append([post.title, post.id, post.author, post.score, post.url, post.selftext, post.created_utc])
    posts = pd.DataFrame(posts,columns=['title', 'id', 'author', 'score', 'url', 'selftext', 'created_utc'])
    
    print(posts)
    
if __name__ == "__main__":
    reddit_page = sys.argv[1]
    reddit_api()
    reddit_data_extraction(reddit_page)
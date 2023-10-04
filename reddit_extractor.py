from operator import concat
import praw
import pandas as pd
import numpy as np

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
    hot_posts=[]
    top_posts=[]
    new_posts=[]
    column=['title', 'selftext', 'created_utc']
    reddit_posts = reddit.subreddit(reddit_page)
    for post in reddit_posts.hot(limit=None):
        hot_posts.append([post.title, post.selftext, post.created_utc])
    for post in reddit_posts.top(limit=None):
        top_posts.append([post.title, post.selftext, post.created_utc])
    for post in reddit_posts.new(limit=None):
        new_posts.append([post.title, post.selftext, post.created_utc])
    hot_posts = pd.DataFrame(hot_posts,columns=column)
    hot_posts['category'] = 'hot'
    hot_posts.insert(loc=0, column='subreddit', value=reddit_page)
    top_posts = pd.DataFrame(top_posts,columns=column)
    top_posts['category'] = 'top'
    top_posts.insert(loc=0, column='subreddit', value=reddit_page)
    new_posts = pd.DataFrame(new_posts,columns=column)
    new_posts['category'] = 'new'
    new_posts.insert(loc=0, column='subreddit', value=reddit_page)
    concatanated_posts = pd.concat([hot_posts, top_posts, new_posts], ignore_index=True).reset_index(drop=True)
    clean_data(concatanated_posts)
    concatanated_posts.to_csv('{}_reddit_posts.csv'.format(reddit_page))
    
def clean_data(df):
    df['datetime'] = pd.to_datetime(df['created_utc'],unit='s')
    df['datetime'] = df['datetime'].astype(str)
    df = df.drop('created_utc', axis = 1)
    df = df.replace(r'^\s*$', np.nan, regex=True)
    
if __name__ == "__main__":
    reddit_api()
    file_path = 'subreddits.txt'
    with open(file_path, 'r') as file:
        for line in file:
            print("------------------------------------------------")
            print("Subreddit: {}".format(line))
            try:
                reddit_data_extraction(line)
            except Exception as e:
                print("Data Extraction Failed: {}".format(e))
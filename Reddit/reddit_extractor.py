from operator import concat
import praw
import pandas as pd
import numpy as np
import mysql.connector
import configparser
import sqlalchemy

user_agent = "Scrapper 1.0 by /u/willissssa"
client_id = "7yQTXog0_Zi1dAWu0WkMkg"
client_secret="__whBicqP2M30uNn1u-lvqfNUUap1Q"

def connect_to_db():
    config = configparser.ConfigParser()
    config.read('config.ini')
    default = config['DEFAULT-SQLCONNECTOR']
    return mysql.connector.connect(
        host=default['DB_HOST'],
        user=default['DB_USER'],
        password=default['DB_PASSWORD'],
        database=default['DB_DATABASE']
    )
    
def execute_query(connection, query):
    cursor = connection.cursor()
    cursor.execute(query)
    
# def check_table_exist_else_create(connection, table):
#     check_table_query = """
#             CREATE TABLE IF NOT EXISTS `{}` ( 
#             `title` longtext NOT NULL, 
#             `selftext` longtext NOT NULL, 
#             `datetime` datetime NOT NULL, 
#             `category` varchar(45) NOT NULL, 
#             `subreddit` varchar(45) NOT NULL);""".format(table)
#     execute_query(connection, check_table_query)
    
def insert_df_to_table(df, table):
    config = configparser.ConfigParser()
    config.read('config.ini')
    default = config['DEFAULT-SQLALCHEMY']
    engine = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                               format(default['DB_USER'], default['DB_PASSWORD'], 
                                                      default['DB_IP'], default['DB_DATABASE']))
    df.to_sql(con=engine, name=table, if_exists='append', index=False)
    
def reddit_api():
    return praw.Reddit(
        client_id = client_id,
        client_secret = client_secret,
        user_agent = user_agent
    )
    
def reddit_data_extraction(reddit, reddit_page, table):
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
    hot_posts['subreddit'] = reddit_page
    top_posts = pd.DataFrame(top_posts,columns=column)
    top_posts['category'] = 'top'
    top_posts['subreddit'] = reddit_page
    new_posts = pd.DataFrame(new_posts,columns=column)
    new_posts['category'] = 'new'
    new_posts['subreddit'] = reddit_page
    concatanated_posts = pd.concat([hot_posts, top_posts, new_posts], ignore_index=True).reset_index(drop=True)
    concatanated_posts['datetime'] = pd.to_datetime(concatanated_posts['created_utc'],unit='s')
    concatanated_posts['datetime'] = concatanated_posts['datetime'].astype(str)
    concatanated_posts = concatanated_posts.drop('created_utc', axis = 1)
    concatanated_posts = concatanated_posts.replace(r'^\s*$', np.nan, regex=True)
    # concatanated_posts.to_csv('{}_reddit_posts.csv'.format(reddit_page.strip()))
    # check_table_exist_else_create(connection, table)
    insert_df_to_table(concatanated_posts, table)
    
if __name__ == "__main__":
    connection = connect_to_db()
    reddit = reddit_api()
    table = 'reddit_data'
    file_path = 'subreddits.txt'
    with open(file_path, 'r') as file:
        for line in file:
            print("------------------------------------------------")
            print("Subreddit: {}".format(line))
            try:
                reddit_data_extraction(reddit, line, table)
            except Exception as e:
                print("Data Extraction Failed: {}".format(e))
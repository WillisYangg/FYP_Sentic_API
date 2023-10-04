import tweepy
import configparser
import sys

def twitter_data_extraction():
    global twitter_api
    config = configparser.ConfigParser()
    config.read('config.ini')
    default = config['DEFAULT']

    auth = tweepy.OAuthHandler(default['consumer_key'], default['consumer_secret'])   
    auth.set_access_token(default['access_token'], default['access_token_secret']) 

    twitter_api = tweepy.API(auth)

def hashtag_extract(hashtag):
    hashtag_tweets = tweepy.Cursor(twitter_api.search, q=hashtag,tweet_mode='extended').items(5)
    return hashtag_tweets


if __name__ == "__main__":
    hashtag = sys.argv[1]
    twitter_data_extraction()
    hashtag_extract(hashtag)
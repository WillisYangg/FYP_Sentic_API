from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from getpass import getpass
from time import sleep
import pandas as pd
import configparser
import sqlalchemy
import mysql.connector
from datetime import date
import sys

today = date.today()

PATH = 'Twitter/chromedriver'
username = 'willissssa'
password='Drogba11&'
# search_query='depression'

target_url = "https://twitter.com"

def connect_to_db(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
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
    
def insert_df_to_table(df, table, config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    default = config['DEFAULT-SQLALCHEMY']
    engine = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                               format(default['DB_USER'], default['DB_PASSWORD'], 
                                                      default['DB_IP'], default['DB_DATABASE']))
    df.to_sql(con=engine, name=table, if_exists='append', index=False)

def twitter_data_extraction_from_hashtags(search_query, table):
    service = Service(executable_path=PATH)
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(target_url)
    sleep(5)

    driver.find_element("xpath", "//*[text()='Sign in']").click()
    sleep(5)

    driver.find_element("xpath", "//input[@name='text']").click()
    driver.find_element("xpath", "//input[@name='text']").send_keys(username)
    driver.find_element("xpath", "//*[text()='Next']").click()
    sleep(5)

    driver.find_element("xpath", "//input[@name='password']").click()
    driver.find_element("xpath", "//input[@name='password']").send_keys(password)
    driver.find_element("xpath", "//*[text()='Log in']").click()
    sleep(5)

    driver.find_element("xpath", "//input[@data-testid='SearchBox_Search_Input']").click()
    driver.find_element("xpath", "//input[@data-testid='SearchBox_Search_Input']").send_keys(search_query)
    driver.find_element("xpath", "//input[@data-testid='SearchBox_Search_Input']").send_keys(Keys.RETURN)
    sleep(5)

    driver.find_element("xpath", "//span[contains(text(),'Latest')]").click()
    sleep(5)

    tweets = driver.find_elements("xpath", "//article[@data-testid='tweet']")
    # sleep(5)

    TimeStamps=[]
    Tweets=[]

    while True:
        for tweet in tweets:
            TimeStamp = driver.find_element("xpath", ".//time").get_attribute('datetime')
            TimeStamps.append(TimeStamp)
            Tweet = driver.find_element("xpath", ".//div[@data-testid='tweetText']").text
            Tweets.append(Tweet)
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
        sleep(5)
        tweets = driver.find_elements("xpath", "//article[@data-testid='tweet']")
        Tweets2 = list(set(Tweets))
        if len(Tweets2) > 5:
            break

    driver.close()

    df = pd.DataFrame(zip(TimeStamps,Tweets),columns=['TimeStamps','Tweets'])
    df['Date Scraped'] = today
    df = df.drop_duplicates().reset_index(drop=True)

    # df.to_csv("{}_twitter.csv".format(search_query))
    
    insert_df_to_table(df, table)
    
def twitter_data_extraction_from_page(search_query, table):
    service = Service(executable_path=PATH)
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(target_url)
    sleep(5)

    driver.find_element("xpath", "//*[text()='Sign in']").click()
    sleep(5)

    driver.find_element("xpath", "//input[@name='text']").click()
    driver.find_element("xpath", "//input[@name='text']").send_keys(username)
    driver.find_element("xpath", "//*[text()='Next']").click()
    sleep(5)

    driver.find_element("xpath", "//input[@name='password']").click()
    driver.find_element("xpath", "//input[@name='password']").send_keys(password)
    driver.find_element("xpath", "//*[text()='Log in']").click()
    sleep(5)

    driver.find_element("xpath", "//input[@data-testid='SearchBox_Search_Input']").click()
    driver.find_element("xpath", "//input[@data-testid='SearchBox_Search_Input']").send_keys(search_query)
    driver.find_element("xpath", "//input[@data-testid='SearchBox_Search_Input']").send_keys(Keys.RETURN)
    sleep(5)
    
    driver.find_element("xpath", "//span[contains(text(),'People')]").click()
    sleep(5)
    
    profile = driver.find_element("xpath", '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/section/div/div/div[1]/div/div/div/div/div[2]/div[1]/div[1]/div/div[1]/a/div/div[1]/span/span[1]')
    profile.click()
    sleep(5)
    
    tweets = driver.find_elements("xpath", "//article[@data-testid='tweet']")
    # sleep(5)

    TimeStamps=[]
    Tweets=[]
    
    while True:
        for tweet in tweets:
            TimeStamp = driver.find_element("xpath", ".//time").get_attribute('datetime')
            TimeStamps.append(TimeStamp)
            Tweet = driver.find_element("xpath", ".//div[@data-testid='tweetText']").text
            Tweets.append(Tweet)
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
        sleep(5)
        tweets = driver.find_elements("xpath", "//article[@data-testid='tweet']")
        Tweets2 = list(set(Tweets))
        if len(Tweets2) > 5:
            break
        
    driver.close()

    df = pd.DataFrame(zip(TimeStamps,Tweets),columns=['TimeStamps','Tweets'])
    df['Date Scraped'] = today
    df = df.drop_duplicates().reset_index(drop=True)
    
    insert_df_to_table(df, table, config_file)
    
def scrape_from_twitter(file_path, table):
    with open(file_path, 'r') as file:
        for search_query in file:
            print("------------------------------------------------")
            print("Search Query: {}".format(search_query))
            try:
                # twitter_data_extraction_from_hashtags(search_query, table)
                twitter_data_extraction_from_page(search_query, table)
            except Exception as e:
                print("Data Extraction Failed: {}".format(e))
    
if __name__ == "__main__":
    file_path = sys.argv[1]
    config_file = sys.argv[2]
    table = 'twitter_data'
    scrape_from_twitter(file_path, table)
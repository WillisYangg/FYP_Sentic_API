from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from getpass import getpass
from time import sleep
import pandas as pd

PATH = './chromedriver'
username = 'willissssa'
password=getpass()
# search_query='depression'

target_url = "https://twitter.com"

def twitter_data_extraction(search_query):
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
        if len(Tweets2) > 9:
            break

    driver.close()

    df = pd.DataFrame(zip(TimeStamps,Tweets),columns=['TimeStamps','Tweets'])
    df = df.drop_duplicates().reset_index(drop=True)

    df.to_csv("{}_twitter.csv".format(search_query))
    
if __name__ == "__main__":
    file_path = 'twitter_search.txt'
    with open(file_path, 'r') as file:
        for search_query in file:
            print("------------------------------------------------")
            print("Search Query: {}".format(search_query))
            try:
                twitter_data_extraction(search_query)
            except Exception as e:
                print("Data Extraction Failed: {}".format(e))
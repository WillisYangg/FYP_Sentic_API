from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from getpass import getpass
from time import sleep, time
import pandas as pd
import os

PATH = './chromedriver'
username = "willissssa"
password = getpass()
# search_query='depression'

target_url = "https://instagram.com"

destination = './photos'

if not os.path.exists(destination):
    os.mkdir(destination)
    print("Directory {} has been created".format(destination))
else:
    print("Directory {} exists!")
    
service = Service(executable_path=PATH)
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

driver.get(target_url)
sleep(5)

user_name = driver.find_element("xpath", "//input[@name='username']")
user_name.send_keys(username)
sleep(5)

pw = driver.find_element("xpath", "//input[@name='password']")
pw.send_keys(password)
pw.send_keys(Keys.ENTER)
sleep(5)

#save login information box
not_now = driver.find_element("xpath", "//*[text()='Not now']")
not_now.click()
sleep(5)

#turn on notification box
Not_Now = driver.find_element("xpath", "//*[text()='Not Now']")
Not_Now.click()
sleep(5)

hashtag = "fashion"
driver.get("https://www.instagram.com/explore/tags/" + hashtag + "/")
sleep(5)

# search = driver.find_element("xpath", "//input[@aria-label='Search input']")
# search.clear()
# search.send_keys(search_query)
# search.send_keys(Keys.ENTER)
# sleep(5)


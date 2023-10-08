# This instagram extractor is used to extract more images for image model training to classify obese and healthy people
# Focus: Body Dysmorphia

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from getpass import getpass
from time import sleep, time
import pandas as pd
import os
import wget

PATH = './chromedriver'
username = "willissssa"
password = getpass()
# search_query='obese'

target_url = "https://instagram.com"
    
def instagram_data_extractor(search_query, destination):
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

    driver.get("https://www.instagram.com/explore/tags/" + search_query + "/")
    sleep(5)
    
    image_links=[]
    n_scrolls = 3
    for i in range(1, n_scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(5)
        
    anchors = driver.find_elements(By.TAG_NAME, "a")
    anchors = [a.get_attribute("href") for a in anchors]
    anchors = [a for a in anchors if a.startswith("https://www.instagram.com/p/")]
    
    image_links += anchors
    
    print("Image Links: {}".format(image_links))
    print("Total number of images: {}".format(len(image_links)))
    
    image_source=[]
    for link in image_links:
        driver.get(link)
        sleep(5)
        
        images = driver.find_elements(By.TAG_NAME, 'img')
        
        for image in images:
            source = image.get_attribute('src')
            if str(source).startswith("https://scontent.cdninstagram.com/v/"):
                image_source.append(source)
                break
    
    # print("Image Source: {}".format(image_source))
    print("Total number of image sources: {}".format(len(image_source)))
    
    for idx, image in enumerate(image_source):
        save_as = os.path.join(destination + str(idx) + '.jpg')
        wget.download(image, save_as)

if __name__ == "__main__":
    file_path = 'instagram_hashtag.txt'
    with open(file_path, 'r') as file:
        for search_query in file:
            destination = './photos/{}/'.format(search_query)
            if not os.path.exists(destination):
                os.mkdir(destination)
                print("Directory {} has been created".format(destination))
            else:
                print("Directory {} exists!")
            instagram_data_extractor(search_query, destination)
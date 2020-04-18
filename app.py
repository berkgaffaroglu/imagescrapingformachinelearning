from bs4 import BeautifulSoup
import requests
import re
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import bingscraper as bs
import os
browser = webdriver.Chrome()
browser.set_window_size(150,150)
browser.set_window_position(-300,-300)
imageTypes = ['.jpg','.png','.jpeg']
def getTag():
    tagList = list()
    src = requests.get('https://business.pinterest.com/en/blog/trending-searches-for-april-2020').text
    soup = BeautifulSoup(src,'lxml')
    links = soup.findAll('a')
    for link in links:
        if link.span is not None:
            string = f'{link.span.u}'

            setting = re.compile('<.*?>')
            string = re.sub(setting, '',string)
            if string != 'None':
                tagList.append(string)
    return tagList


def search(item):
    browser.get('https://www.bing.com/images/search?q=a&scope=images&form=QBLH&sp=-1&pq=&sc=0-0&qs=n&sk=&cvid=7E2AA6CD6F924FCFB8CABABF4655BDF7')
    time.sleep(5)
    pythonbutton = browser.find_element_by_xpath('//*[@id="sb_form_q"]')
    pythonbutton.send_keys(Keys.BACKSPACE)
    pythonbutton.send_keys(item)
    pythonbutton = browser.find_element_by_xpath('//*[@id="sb_form_go"]')
    pythonbutton.click()
    time.sleep(2)
    pythonbutton = browser.find_element_by_xpath('//*[@id="fltIdtLnk"]')
    pythonbutton.click()
    time.sleep(2)
    pythonbutton = browser.find_element_by_xpath('//*[@id="ftrB"]/ul/li[4]/span')
    pythonbutton.click()
    time.sleep(2)
    pythonbutton = browser.find_element_by_xpath('//*[@id="ftrB"]/ul/li[4]/div/div/a[4]')
    pythonbutton.click()
    return browser.current_url

def download(tag, url):
    bs.scrape(tag).image(url)  # For Image Scraping.

def directoryOrder(tag):
   dir_name = tag.replace(" ", "_").lower()
   os.chdir(dir_name)
   i = 0
   for file in os.listdir():

       fileName, extension = os.path.splitext(file)
       if extension in imageTypes:
           i+=1
           newName = f'{tag} ({i}).jpg'
           os.rename(file,newName)
       else:
           os.remove(file)
   os.chdir("..")


def run():
    tagList = getTag()
    tag = tagList[0]
    url = search(tagList[0])
    download(tag, url)
    directoryOrder(tag)
    print(os.getcwd())
try:
    run()
except Exception as e:
    print(e)
    browser.close()


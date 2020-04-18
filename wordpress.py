from selenium import webdriver
import time
import os
browser = webdriver.Chrome()

def upload(tag):
    browser.get('https://hizliresim.com/')
    time.sleep(3)
    dir_name = tag.replace(" ", "_").lower()
    os.chdir(dir_name)
    for image in os.listdir():
        browser.find_element_by_id('local_files').send_keys(f'/Users/teknosa/PycharmProjects/pinterestBot/{dir_name}/{image}')


upload('cat')
from bs4 import BeautifulSoup
import requests
import re
import bingscraper as bs
import os
from PIL import Image,ImageOps,ImageFilter,ImageEnhance
import datetime
imageTypes = ['.jpg','.png','.jpeg']
def search(item):
    query = item
    query = query.split()
    query = '+'.join(query)
    url = f'https://www.bing.com/images/search?&q={query}&qft=+filterui:aspect-tall&FORM=IRFLTR'
    return url

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
           basewidth = 800
           baseheight = 1200
           img = Image.open(file)
           img = ImageOps.mirror(img)
           img = img.filter(ImageFilter.GaussianBlur(radius=0.3))
           img = ImageEnhance.Brightness(img).enhance(1)
           img = ImageEnhance.Color(img).enhance(0.7)
           img = img.resize((basewidth, baseheight), Image.ANTIALIAS)
           try:
               img.save(f'{file}')
           except Exception as e:
               img = img.convert('RGB')
               img.save(f'{file}')
           newName = f'{tag} ({i}).jpg'
           os.rename(file, newName)
       else:
           os.remove(file)
   os.chdir("..")

def run(tag):
    if tag is not -1:
        first = datetime.datetime.today()
        url = search(tag)
        download(tag, url)
        directoryOrder(tag)
        from wordpress import upload
        upload(tag) # will be change
        last = datetime.datetime.today()
        took = last - first
        print(f'{took.seconds}.{took.microseconds} saniye sürdü.')
        os.chdir('..')
tag = 'sword'
tagList = list()
with open('tags.txt','r') as file:
    tags = file.read()
    tags = tags.split(',')
    for tag in tags:
        tagList.append(tag)

for actualTag in tagList:
    run(actualTag)


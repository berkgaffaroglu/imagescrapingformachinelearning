from bs4 import BeautifulSoup
import requests
import re
import bingscraper as bs
import os
from imageManipulation import imageManipulation

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
           newName = f'{tag} ({i}).jpg'
           os.rename(file,newName)
       else:
           os.remove(file)
   os.chdir("..")


def run(tag):
    url = search(tag)
    print(f'Arama indiriliyor: {tag}')
    download(tag, url)
    print(f'Isımler degistiriliyor.')
    directoryOrder(tag)
    print('Resimlerle oynanıyor..')
    imageManipulation(tag)
    print(f'Resimler ters çevirildi, blur eklendi ve parlaklık arttırıldı.')
try:
    run(input(': '))
except Exception as e:
    print(e)


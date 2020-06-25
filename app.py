import os
import datetime
import time
from selenium import webdriver
import random
import shutil
from classes import Site
import json
from PIL import Image,ImageOps,ImageFilter,ImageEnhance,ImageDraw
from wordpress import upload
imageTypes = ['.jpg','.png',]

with open('config.json') as settings:
    settingsData = json.load(settings)
for setting in settingsData['ayarlar']:
    if setting['mirror'] == 'true':
        mirror = True
    elif setting['mirror'] == 'false':
        mirror = False
    categoryID = setting['categoryID']

def deleteFile(tag):
    time.sleep(2)
    dir_name = tag.replace(' ','_')
    try:
        dest = os.getcwd() + f'\\{dir_name}'
        shutil.rmtree(dest)
    except Exception as e:
        print('Dosya silinemedi!')

def moveIt(tag):
    
    dir_name = tag.replace(' ','_')
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    os.chdir('workspace')
    for image in os.listdir():
        source = os.getcwd() + f'\\{image}'
        os.chdir('..')
        dest = os.getcwd() + f'\\{dir_name}' + f'\\{image}'
        os.chdir('workspace')
        shutil.move(source,dest)
    os.chdir('..')
    
    
    
def sizeElemination():
    os.chdir('workspace')
    for image in os.listdir():
        from fileSize import getSize
        fileName,extension = os.path.splitext(image)
        if extension in imageTypes:
            pass
        else:
            os.remove(image)
    os.chdir('..')

def changeNames(tag,currentWebSite):
    randomNumber = 25
    os.chdir('workspace')
    imageCount = 1
    namingCount = 1
    for image in os.listdir():
        fileName,extension = os.path.splitext(image)
        newName = f'{tag} ({namingCount}){extension}'
        imageCount+=1
        if imageCount > randomNumber:
            os.remove(image)
        else:
            img = Image.open(image)
            if mirror:
                img = ImageOps.mirror(img)
            try:
                img = img.filter(ImageFilter.GaussianBlur(radius=0.3))
                img = ImageEnhance.Brightness(img).enhance(0.8)
                img = ImageEnhance.Color(img).enhance(0.7)
            except Exception as e:
                print('Gaussian blur olmadi ',e)
            
            try:
                
                if img.size[0] > img.size[1]:
                    os.remove(image)
                else:
                    namingCount+=1
                    if extension == '.png':
                        img = img.convert('RGBA')
                        img.save(image)
                    if extension == '.jpg' or extension == '.jpeg':
                        img = img.convert('RGB')
                        img.save(image)
                    os.rename(image,newName)
            except Exception as e:
                print(e)
    os.chdir('..')
                

def run(tag,mode,site):
    
    sizeElemination()
    print('Size Eleme yapildi')
    changeNames(tag,site)
    print('Isım degistirme yapildi')
    moveIt(tag)
    print('Tasima yapildi')
    if mode == 'a':
        try:
            upload(tag,site,categoryID)
        except Exception as e:
            print(e)
        print(f'Post atildi')
        deleteFile(tag)
        print(f'Dosya silindi.')












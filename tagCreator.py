import csv
import string
def getFinishedTagList():
    try:
        with open('lastTag.txt','r') as file3:
            finishedTagList = list()
            tags = file3.read()
            tagString = f'{tags}'
            tagList = tagString.split(',')
            for tag in tagList:
                finishedTagList.append(tag)
        return finishedTagList




    
    except Exception as e:
        print(e)
            
def writeLastTag(tag):
    with open('lastTag.txt','a') as file2:
        file2.write(f'{tag},')

def getTagList():
    with open('keywords.csv','r') as file:
        csvreader = csv.DictReader(file)
        tagList = list()
        for line in csvreader:
            keyword = line['keyword'].split('ile ilgili')[0].strip()
            keyword = string.capwords(keyword)
            if keyword in getFinishedTagList():
                pass
            else:
                tagList.append(keyword)
            
    return tagList





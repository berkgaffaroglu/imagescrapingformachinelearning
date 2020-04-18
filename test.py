import os
from PIL import Image
imageTypes = ['.jpg','.png','.jpeg']
size2to3 = (800,1200)
def imageManipulation(tag):
    dir_name = tag.replace(" ", "_").lower()
    os.chdir(dir_name)
    i = 0
    for file in os.listdir():
        fileName, extension = os.path.splitext(file)
        if extension in imageTypes:
            # creating a object
            print(file)
            image = Image.open(file)
            MAX_SIZE = (100, 100)

            image.resize(MAX_SIZE)

            # creating thumbnail
            image.save('newONE.jpg')

        else:
            os.remove(file)
    os.chdir("..")

imageManipulation('curated, inspiring ideas')

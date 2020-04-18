import os
from PIL import Image,ImageOps,ImageFilter
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

            basewidth = 800
            baseheight = 1200
            img = Image.open(file)
            img = ImageOps.mirror(img)
            img = img.filter(ImageFilter.GaussianBlur(radius=0.5))
            img = img.resize((basewidth, baseheight), Image.ANTIALIAS)

            img.save(f'{fileName}{extension}')

        else:
            os.remove(file)
    os.chdir("..")

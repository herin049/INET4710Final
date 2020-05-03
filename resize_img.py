from PIL import Image
import os, sys

path = "images/"
dirs = os.listdir(path)


for item in dirs:
    if os.path.isfile(path+item):
        try:
            im = Image.open(path+item)
            f, e = os.path.splitext(path+item)
            imResize = im.resize((128,128), Image.ANTIALIAS)
            imResize.save(f+".jpg", 'JPEG', quality=90)
        except:
            continue

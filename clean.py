from PIL import Image
import os, sys

path = "images/"
dirs = os.listdir(path)


for item in dirs:
    if os.path.isfile(path+item):
        try:
            if(item.__contains__("jpg")):
                continue
            else:
                os.remove(path+item)
        except:
            continue
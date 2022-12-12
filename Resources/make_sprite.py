#!/usr/bin/python
import sys,os
import math
from PIL import Image
from os import listdir
from os.path import isfile, join
from natsort import natsorted



def createSpriteSheet(listofimages, name='sprite', cols=None, rows=None, frame_width=128, frame_height=128):

    if cols == None:
        cols = len(listofimages)

    if rows == None:
        rows = int(math.ceil(len(listofimages) / cols))

    maxw = 0
    maxh = 0

    frames = []
    for p in listofimages:
        im = Image.open(p)
        w,h = im.size
        print(w,h)
        if w > maxw:
            maxw = w
        if h > maxh:
            maxh = h
        frames.append(im)


    x = 0
    y = 0
    i = 0

    width = frame_width * cols
    height = frame_height * rows

    sprite = Image.new('RGBA', (width, height),(255, 255, 255, 0))
   
    for f in frames:
        w,h = f.size
        fwr = w/maxw
        fhr = h/maxh
        f.thumbnail((int(frame_width*fwr),int(frame_height*fhr)), Image.ANTIALIAS)
        sprite.paste(f, (x, y))
        x += frame_width
        i += 1
        if i % cols == 0:
            x = 0
            y += frame_height

    sprite.save(name+".png")

def grabName(name,sep,index):
    name = name.split(sep)
    return name[index]

if __name__=='__main__':
    
    if len(sys.argv) < 2:
        print("Usage: wrong")
        sys.exit(0)
    mypath = sys.argv[1]
    listofimages = [join(mypath, f) for f in listdir(mypath) if isfile(join(mypath, f))]

    listofimages = natsorted(listofimages)

    oldName = grabName(os.path.basename(listofimages[0]),' ',0)
    j = 0
    for i in range(len(listofimages)):
        name = grabName(os.path.basename(listofimages[i]),' ',0)
        if not name == oldName:
            createSpriteSheet(listofimages[j:i],oldName)
            oldName = name
            j = i
    createSpriteSheet(listofimages[j:i],oldName)

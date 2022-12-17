"""
Program: spriter.py

Extract: 
    Extracting will take a sprite sheet (basic one) with consistent size frames and turn it into 
    a directory of individual images. It assumes a table format (rows and columns). The link below
    points to a pacman sprite sheet with 9 rows and 17 columns. However columns 13-17 are used 
    for a single sprite with nothing below row 1. 

    https://cs.msutexas.edu/~griffin/zcloud/zcloud-files/pacman_ghosts.png

    This script doesn't handle URL's, so you would need to copy whatever image locally. 

    Example 1:  extract all the images (including a bunch of blank ones at the end)

        python spriter.py action=extract inpath=pacman_ghosts.png outpath=pacman_ghosts_folder\
             name=pacman_orange rows=9 cols=17 frame_width=40 frame_height=40 direction=xy

        This wouldn't much good if you wanted to seperate each color pacman. See following...

    Example 2: extract pink pacman. Uses same command as above but only reads three columns 
        and starts with an xoffset of 120 (skipping red)

        python spriter.py action=extract inpath=pacman_ghosts.png outpath=pacman_pink_folder\
             name=pacman_pink rows=9 cols=3 frame_width=40 frame_height=40 direction=xy xoffset=120

    Example 3: extract ghost dying

        python spriter.py action=extract inpath=pacman_ghosts.png outpath=pacman_ghosts_folder\
             name=pacman_pink rows=1 cols=5 frame_width=40 frame_height=40 direction=xy xoffset=480

Create:
    Creating a spritesheet takes a folder of images and processes them based on their alphanumeric order. 
    You tell the script how many rows and columns you want and a frame size, and it will put all images 
    in the folder on a single image sheet in order (row wise or column wise). 

    Example:
        If you have the orange pacman in a folder number orange_001.png orange_002.png ... all the way 
        to orange_027.png and they are ordered like the top 3 orange sprites are 1-3 and the bottom row 
        of orange is 25-27, then you could re-create a sprite sheet just for orange (using your images) 
        like this:

        python spriter.py action=create inpath=pacman_ghosts_folder [outpath=pacman_ghosts_folder] name=pacman_orange_sprite.png\
             rows=9 cols=3 frame_width=40 frame_height=40 direction=xy

        https://cs.msutexas.edu/~griffin/zcloud/zcloud-files/pacman_spritesheet_xydir.png

        If you swap xy => yx this is what you get:

        https://cs.msutexas.edu/~griffin/zcloud/zcloud-files/pacman_spritesheet_yxdir.png

        If you don't provide an out path it will assume same directory as in path and call the new file sprite_sheet_<timestamp>.png 
        where timestamp is an integer value. 

"""
import sys,os
import math
from PIL import Image
from os import listdir
from os.path import isfile, join
from natsort import natsorted
import glob
import time;

def canBeInt(val):
    try:
        val = int(val)
        print("trying")
    except ValueError:
        print("failed")
        return val
    return val


class SpriteSheet(object):

    def __init__(self,**kwargs):
        """ Takes a sprite sheet thats layed out in a consistent manor (same size tiles), 
            it will take each "tile" and create a seperate image. 
        Args:
            inpath <string>     : path to input folder
            outpath <string>    : path to outinput folder
            name <string>       : basename to give to each file
            rows <int>          : how many rows in the sheet
            cols <int>          : how many columns in the sheet
            frame_width <int>   : width of frame in pixels
            frame_height <int>  : height of frame in pixels
            direction <xy / yx> : process row then col (xy) or column then row (yx)
            xoffset <int>       : lets you skip frames in x direction
            yoffset <int>       : skip frames in y direction
            isCentered <bool>   : is image centered in each frame
        """
        for k,v in kwargs.items():
            kwargs[k] = canBeInt(v)

        self.inpath = kwargs.get("inpath",None)
        self.outpath = kwargs.get("outpath",None)
        self.name = kwargs.get("name",None)
        self.rows = kwargs.get("rows",None)
        self.cols = kwargs.get("cols",None)
        self.frame_width = kwargs.get("frame_width",None)
        self.frame_height = kwargs.get("frame_height",None)
        self.direction = kwargs.get("direction",None)
        self.xoffset = kwargs.get("xoffset",0)
        self.yoffset = kwargs.get("yoffset",0)
        self.xgap = kwargs.get("xgap",0)
        self.ygap = kwargs.get("ygap",0)
        self.xborder = kwargs.get("xborder",0)
        self.yborder = kwargs.get("yborder",0)
        self.centerit = kwargs.get("centerit",False)
        self.gravity = kwargs.get("gravity","center")

        print(self.inpath)

        self.im = self._openImage(self.inpath)

        self._checkOutPath()


    def _openImage(self,inpath):
        """
        """        
        if not os.path.isfile(inpath):
            print(f"{inpath} is not a proper file...")
            sys.exit()

        self.im = Image.open(inpath)

        return self.im

    def _checkOutPath(self):
        """
        """
        # checking if outpath exists, if not create it ... 
        if not os.path.isdir(self.outpath):
            ans = input(f"{self.outpath} is not a directory! Would you like me to create it? [Y/n]:")
        
            if ans == "" or ans == "Y" or ans =="y":
                try:
                    os.mkdir(self.outpath)
                except OSError:
                    print (f"Creation of the directory {self.outpath} failed!")
                else:
                    print (f"Successfully created the directory {self.outpath}")

    def _sequence_num(self, n=0,digits=3):
        """ Returns a zero padded string.
            Example: sequence(234,7) would return 0000234
        """
        return str(n).zfill(digits)


    def _centerIt(self,im,gravity="center"):
        frame_im = im.crop(im.getbbox())

        return self._addMargin(frame_im,gravity)

    def _addMargin(self,im, gravity="center"):
        """
        Args:
            im (PIL) : Pil image resource
            gravity (str) : center, north, south, west
        """
        newImg = Image.new('RGBA', (self.frame_width, self.frame_height), (255, 0, 0, 0))

        imwidth, imheight = im.size

        left = (self.frame_width // 2) - (imwidth//2)
        top = (self.frame_height // 2) - (imheight//2)

        if gravity=="north":
            top = 0
        elif gravity =="south":
            top = (self.frame_height) - (imheight)
        elif gravity =="east":
            left = (self.frame_width) - (imwidth)
        elif gravity =="west":
            left = 0

        newImg.paste(im, (left, top))

        return newImg

    def _saveFrame(self,x, y,sequence,quality=95):
        """Save a sprite frame by cropping then maybe centering based on args.
        Args:
            x (int) : x pixel
            y (int) : y pixel
            sequenct (int) : frame number
            quality (int) : image quality 0-100
        """
        frame_im = self.im.crop((x, y, x+self.frame_width, y+self.frame_height))

        # center the sprite frame if tasked to
        if self.centerit:
            
            frame_im = self._centerIt(frame_im,self.gravity)


        name = os.path.join(self.outpath,self.name+'_'+sequence+".png")

        print(f"saving: {name}")

        frame_im.save(name, quality=quality)


    def explodeSpriteSheet(self):

        count = 1
        
        # Traverse sheet checking below if we need to process row-wise or column-wise
        for i in range(self.rows):

            # row-wise / column-wise
            if self.direction == 'xy':
                y = i * self.frame_height + (self.ygap * i) + self.yborder
            else:
                x = i * self.frame_height

            for j in range(self.cols):

                # row-wise / column-wise
                if self.direction == 'xy':
                    x = j * self.frame_width + (self.xgap * j) + self.xborder
                else:
                    y = j * self.frame_width

                # format count to use as filename
                sequence = self._sequence_num(count)

                # jump to proper xy location
                x += self.xoffset
                y += self.yoffset

                print(f"processing frame {sequence} at[{x},{y}]")
                
                # save the sprite frame
                self._saveFrame(x,y,sequence)

                count += 1

def createSpriteSheet(**kwargs):
    """ Takes a sprite sheet thats layed out in a consistent manor (same size tiles), 
        it will take each "tile" and create a seperate image. 
        Params:
            inpath <string>     : path to input folder
            outpath <string>    : path to outinput folder
            rows <int>          : how many rows in the sheet
            cols <int>          : how many columns in the sheet
            frame_width <int>   : width of frame in pixels
            frame_height <int>  : height of frame in pixels
            direction <xy / yx> : process row then col (xy) or column then row (yx)
            image_type <string> : default png 
    """
    inpath = kwargs.get("inpath",None)
    outpath = kwargs.get("outpath",None)
    rows = kwargs.get("rows",None)
    cols = kwargs.get("cols",None)
    frame_width = kwargs.get("frame_width",None)
    frame_height = kwargs.get("frame_height",None)
    direction = kwargs.get("direction",None)
    image_type = kwargs.get("image_type","png")
    
    ts = time.time()
    ts = int(ts)

    if outpath == None:
        outpath = os.path.join(inpath,'sprite_sheet_'+str(ts)+'.png')
    else:
        if outpath[-3:] != image_type:
            outpath = os.path.join(outpath,'sprite_sheet_'+str(ts)+'.png')

    if not os.path.isdir(inpath):
        print(f"Error: {inpath} is not a proper folder! ")
        sys.exit()

    frame_width = int(frame_width)
    frame_height = int(frame_height)
    rows= int(rows)
    cols = int(cols)

    images = glob.glob(os.path.join(inpath,f"*.{image_type}"))

    images.sort()

    # calculate sprite sheet size
    width = frame_width * cols
    height = frame_height * rows

    # create a blank image to "paste" on
    spriteimg = Image.new('RGBA', (width, height),(255, 255, 255, 0))

    x = 0
    y = 0
    i = 0
    
    # loop through images and calculate where 
    # to paste image
    for img in images:
        f = Image.open(img)
        w,h = f.size

        # if image is smaller than frame, center it.
        if w < frame_width and h < frame_height:
            tx = x + w // 2
            ty = y + h // 2
        else:
            tx = x
            ty = y
        spriteimg.paste(f, (tx, ty))
        i += 1
        if direction == 'xy':
            x += frame_width 
            if i == cols:
                y += frame_height
                x = 0
                i = 0
        else: # direction == yx
            y += frame_height
            if i == rows:
                x += frame_width
                y = 0
                i = 0

    spriteimg.save(outpath)
    

def mykwargs(argv):
    '''
    Processes argv list into plain args and kwargs.
    Just easier than using a library like argparse for small things.
    Example:
        python file.py arg1 arg2 arg3=val1 arg4=val2 -arg5 -arg6 --arg7
        Would create:
            args[arg1, arg2, -arg5, -arg6, --arg7]
            kargs{arg3 : val1, arg4 : val2}

        Params with dashes (flags) can now be processed seperately
    Shortfalls:
        spaces between k=v would result in bad params
    Returns:
        tuple  (args,kargs)
    '''
    args = []
    kargs = {}

    for arg in argv:
        if '=' in arg:
            key,val = arg.split('=')
            kargs[key] = val
        else:
            args.append(arg)
    return args,kargs

def wrap(line,nl='\n\t'):
    """wraps a string within a terminal window
    """
    nl = nl
    rows, columns = os.popen('stty size', 'r').read().split()

    newline = ''
    line = line.split(" ")
    length = 0
    for item in line:
        item += " "
        if len(item) + length > int(columns):
            newline += nl
            length = 4
        length += len(item)
        newline += item
    return newline


def usage(command=None):

    print(wrap("Usage: python spriter.py action=[extract,create] inpath=string_file outpath=string_folder name=string rows=int cols=int frame_width=int frame_height=int direction=[xy,yx] [xoffset=int] [yoffset=int] [image_type=str]"))

    if command:
        if command == 'extract':
            # Params in square brackets are optional
            # The kwargs function script needs the key value pairs (key=value) to NOT have spaces 
            print(wrap("Example: python spriter.py action=extract inpath=pacman_ghosts.png outpath=pacman_ghosts_folder name=pacman_pink rows=9 cols=3 frame_width=40 frame_height=40 direction=xy xoffset=120"))
            print("")
        else:
            print(wrap("Example: python spriter.py action=create inpath=/path/to/images outpath=/path/to/pacman_pink_ghost.png rows=9 cols=3 frame_width=40 frame_height=40 direction=xy"))
            print("")

    sys.exit()

def checkRequired(required,kwargs):
    """Returns True if all required key values exist.
    """

    for r in required:
     if not kwargs[r]:
        return False

    return True

if __name__=='__main__':
    """
    Sprite maker / extractor.
    """
    argv = sys.argv[1:]

    # process command line args
    args,kwargs = mykwargs(argv)
    
    required = ["action","inpath","outpath","name","rows","cols","frame_width","frame_height","direction"]

    if not checkRequired(required, kwargs):
        usage()

    sheet = SpriteSheet(**kwargs)

    # # make sure action (extract or create) is an argument
    action = kwargs.get("action",None)


    if action == 'extract':

        sheet.explodeSpriteSheet()
        
    # # this is going to be very basic. 
    # # putting specific moves together or anything complicated is 
    # # beyond this script. This will take a folder of images and 
    # # make a sheet with a specified number of rows and columns
    # elif action == 'create':

    #     direction = kwargs.get("direction",None)
    #     image_type = kwargs.get("image_type","png")

    #     # make a list to make sure none of these are None :) 
    #     params = [inpath,rows,cols,frame_width,frame_height,direction]

    #     if None in params:
    #         print("Missing a parameter to create a sprite ... ")
    #         usage("create")

    #     # do it!
    #     createSpriteSheet(**kwargs)

""" 
Resize tiles from one size to another. You never want to go bigger, maybe slightly, but not too much. 
I originally used imageMagick and fired off a bash call, but I figure if any of you wanted to use it, 
I should use PIL a python image library. Which also means you need to install PIL (pip install pillow).
Don't ask :) I don't know where "pillow" comes from. But its a cool lib.

"""
import glob
import os
import sys
from PIL import Image


class ResizeTiles(object):
    """ Resizes a directory of map tiles to a specified size. Will create and write the new images (tiles) to another directory
        or create them and write them in the same directory as the originals. You have the option to add sequence numbers and 
        the image size to the file name.

        Params:
            in_path         <string>    : input directory
            out_path        <string>    : output directory
            sequence_nums   <bool>      : add a sequence number to filename (e.g. 001,002,00N)
            add_size        <bool>      : add image size to filename (e.g. 32x32 24x32 etc)

            size            <int>       : new size of image (will effect width and height)
                OR
            width           <int>       : width of new image 
            height          <int>       : height of new image

        Example:
            python resize_tiles.py in_path=./tiles out_path=./new_folder
                ./tiles/Bush_3.png => ./new_folder/Bush_3.png
                
            python resize_tiles.py in_path=./tiles out_path=./new_folder add_size=True
                ./tiles/Bush_3.png => ./new_folder/Bush_3_20x20.png

            python resize_tiles.py in_path=./tiles out_path=./new_folder add_size=True sequence_nums=True
                ./tiles/Bush_3.png => ./new_folder/Bush_3_20x20_001.png
        
    """
    def __init__(self,**kwargs):
        self.in_path         = kwargs.get('in_path','.')         # input file path
        self.out_path        = kwargs.get('out_path','.')        # output file path
        self.sequence_nums   = kwargs.get('sequence_nums',False) # Add sequence number to outfile name
        self.add_size        = kwargs.get('add_size',False)      # Add size to outfile name
        self.size            = kwargs.get('size',0)              # size (width and height) or image
        self.width           = kwargs.get('width',0)             # width of output image
        self.height          = kwargs.get('height',0)            # height of output image
        self.overwrite       = False                             # overwrite existing files?
        self.start_seq       = 1


        if not os.path.isdir(self.in_path):
            print(f"Error: {self.in_path} is not a valid directory!!")
            sys.exit()

        if not self.dirCheckCreate(self.out_path):
            print(f"Error: {self.out_path} creation seemed to fail. Maybe create it by hand and try again?")
            sys.exit()

        if int(self.size) + int(self.width) + int(self.height) == 0:
            print(f"Error: There is no size or width / height. You must specify a size OR a width and height.")
            sys.exit()
        
        if int(self.size) > 0 and int(self.width) > 0 and int(self.height) > 0:
            print(f"Error: Either choose width and height OR size. Not all three.")
            sys.exit()

        if int(self.size) > 0:
            self.width = int(self.size)
            self.height = int(self.size)
        elif int(self.width) > 0 and int(self.height) > 0:
            self.width = int(self.width)
            self.height = int(self.height)
        else:
            print(f"Error: Choose width and height OR size for your output images.")
            sys.exit()
        

        self.files = glob.glob(os.path.join(self.in_path,"*.png"))
        self.ext = 'png'
        self.outfiles = []
        self.basenames = []

        for f in self.files:
            parts = f.split("/")
            self.basenames.append(parts[-1])

        if self.in_path == self.out_path:
            self.overwrite = self.ask_overwrite()
        
            # overwrite the originals! Ooooh!
            if self.overwrite == 0:
                self.outfiles = self.files[:]
            # add the image size to the outfile name
            elif self.overwrite == 1:
                self.add_size = True
            # add a sequence number to file name
            elif self.overwrite == 2: 
                self.sequence_nums = True
            # add both
            else:
                self.add_size = True
                self.sequence_nums = True


        for of in self.basenames:
            name = of[:-4]
            size = ""
            seq = ""
            if self.add_size:
                size = "_"+self.get_size_string()
            if self.sequence_nums:
                seq = "_"+self.sequence_num()
            new_name = name+size+seq+"."+self.ext
            self.outfiles.append(os.path.join(self.out_path ,new_name))

        for i in range(len(self.files)):
            self.resize_image(self.files[i],self.outfiles[i],self.width,self.height)

    def dirCheckCreate(self,path):
        if os.path.isdir(path):
            return True
        else:
            ans = input(f"\nAttention: {path} is not a directory! Would you like me to create it? [Y/n]:")

            if ans == "" or ans == "Y" or ans =="y":
                try:
                    os.mkdir(path)
                except OSError:
                    print (f"Creation of the directory {path} failed!")
                else:
                    print (f"Successfully created the directory {path}")
                    return True

        return False

    def sequence_num(self,digits=3):
        """ Returns a zero padded string.
            Example: sequence(234,7) would return 0000234
        """
        
        s = str(self.start_seq).zfill(digits)
        self.start_seq += 1
        return s

    def get_size_string(self): 
        return str(self.width)+"x"+str(self.height)

    def ask_overwrite(self):
        """ Asks if user wants to overwrite a directory of images (tiles). 

            Returns:
                0 = If the answer is YES I will overwrite.
                1 = Add size to my outfile name.
                2 = Add sequence number to outfile name.
                3 = Add both to outfile name.
        """
        ans = input(f"\n Your input and output directory's are the same with no filename additions. Do you want to overwrite the original tiles or would you rather me alter the output path? Yes=Overwrite / No=Alter path [y/N]:")

        if ans == "" or ans == "n" or ans =="N":
            ans = input(f"\n You don't want to overwrite the original. Do you want to add size (widthxheight) or sequence number (001,002...) or both? 1=Size, 2=Sequence Number, 3=Both [1,2,3]:")
        else:
            return 0

        return int(ans)

    def generate_output_filenames(self,state):
        pass

    def resize_image(self,tile_in,tile_out,width,height=None):
        """ resizes an image using pil. 
            Params:
                tile_in     <string>    : path to input image
                tile_out    <string>    : path to ouput image
                width       <int>       : width of new image
                height      <int>       : height of new image 
        """
        if not height:
            height = width
        img = Image.open(tile_in)
        img = img.resize((width,height), Image.ANTIALIAS)
        img.save(tile_out) 
        return os.path.isfile(tile_out)

    
################################################################################################################
################################################################################################################
##                   _  __                            
##  _ __ ___  _   _| |/ /_      ____ _ _ __ __ _ ___ 
##  | '_ ` _ \| | | | ' /\ \ /\ / / _` | '__/ _` / __|
##  | | | | | | |_| | . \ \ V  V / (_| | | | (_| \__ \
##  |_| |_| |_|\__, |_|\_\ \_/\_/ \__,_|_|  \__, |___/
##             |___/                        |___/     
                                                                            
def myKwargs(argv):
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

            if str.isdigit(val):
                val = int(val)

            kargs[key] = val

        else:
            args.append(arg)
    return args,kargs

def wrap(line,nl='\n\t'):
    """ wraps a string within a terminal window if necessary
        Params:
            line <string> : the line to be "wrapped"
            nl   <string> : what to end a line with. defaults to newline+tab

    """
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


def line(ch='*',len=80):
    """ Creates a line of a specific character to be used as a visual border
        Won't go beyond the width of the terminal screen.
        Params:
            ch  <string>    : character (or multi chars) to be printed
            len <int>       : the length you want it (gets capped at terminal width)
    """
    rows, columns = os.popen('stty size', 'r').read().split()
    if len > int(columns):
        len = int(columns)
    return ch * int(len)

def usage(command=None):
    print(line('*'))
    print(" Usage:")
    print(wrap("     python resize_tiles.py in_path=directory_path out_path=directory_path [width=N height=N] [size=N] add_size=[True/False] sequence_nums=[True/False]\n"))
    print(ResizeTiles.__doc__)
    print(line('*'))
    sys.exit()

################################################################################################################
################################################################################################################
##                   _       
##   _ __ ___   __ _(_)_ __  
##  | '_ ` _ \ / _` | | '_ \ 
##  | | | | | | (_| | | | | |
##  |_| |_| |_|\__,_|_|_| |_|

if __name__ == '__main__':

    required_params = 2 
    argv = sys.argv[1:] # strip file name (platformGenerator.py) out of args

    # print usage if not called correctly
    if len(argv) < required_params:
        usage()

    # get processed command line args
    args,kwargs = myKwargs(argv)

    ResizeTiles(**kwargs)

""" Helper module stores common functions and config information
    Banners generated with: http://patorjk.com/software/taag/
    Everything is in here right now. 
"""
# Import and initialize the pygame library
import pygame
import random
import json
import pprint
import sys
import os
import math
import glob

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

################################################################################################################
################################################################################################################
#    ____             __ _       
#   / ___|___  _ __  / _(_) __ _ 
#  | |   / _ \| '_ \| |_| |/ _` |
#  | |__| (_) | | | |  _| | (_| |
#   \____\___/|_| |_|_| |_|\__, |
#                          |___/ 

# Keep up with the config stuff. Adding sprite sheets for
# characters and other graphics now

class Config:
    def __init__(self,json=None):
        if not json:
            config = loadJson('config.json')
        elif os.path.isfile(json):
            config = loadJson(json)
        else:
            config = json.loads(json)


################################################################################################################
################################################################################################################
#   ____                     ____             
#  |  _ \ _ __ __ ___      _| __ )  __ _ _ __ 
#  | | | | '__/ _` \ \ /\ / /  _ \ / _` | '__|
#  | |_| | | | (_| |\ V  V /| |_) | (_| | |   
#  |____/|_|  \__,_| \_/\_/ |____/ \__,_|_|   
                                            
def DrawBar(pos, size, borderC, barC, progress):

    # barPos      = (120, 360)
    # barSize     = (200, 20)
    # borderColor = (0, 0, 0)
    # barColor    = (0, 128, 0)

    #DrawBar(barPos, barSize, borderColor, barColor, a/max_a)

    pygame.draw.rect(screen, borderC, (*pos, *size), 1)
    innerPos  = (pos[0]+3, pos[1]+3)
    innerSize = ((size[0]-6) * progress, size[1]-6)
    pygame.draw.rect(screen, barC, (*innerPos, *innerSize))


################################################################################################################
################################################################################################################
#   _                    _     _                 ____             _ _       
#  | |    ___   __ _  __| |   | |___  ___  _ __ / ___| _ __  _ __(_) |_ ___ 
#  | |   / _ \ / _` |/ _` |_  | / __|/ _ \| '_ \\___ \| '_ \| '__| | __/ _ \
#  | |__| (_) | (_| | (_| | |_| \__ \ (_) | | | |___) | |_) | |  | | ||  __/
#  |_____\___/ \__,_|\__,_|\___/|___/\___/|_| |_|____/| .__/|_|  |_|\__\___|
#                                                     |_|                   

def loadJsonSprite(path,filetype=None):
    """ load a json file for whatever you need!
    """
    data = None 


    if not os.path.isdir(path):
        print(f"Error: {path} not a valid folder!")
        sys.exit()

    if not os.path.isfile(os.path.join(path,filetype)):
        print(f"Error: {filetype} is required to be in folder!")
        sys.exit()

    
    # open the json file thats expected to be in the folder
    # and read it in as a string
    f = open(os.path.join(path,filetype),"r")

    data = json.loads(f.read())

    return data

def loadJson(path):
    """ load a json file for whatever you need!
    """
    data = None 

    if os.path.isfile(path):
        f = open(path,"r")

        # make raw string into a python dictionary 
        data = json.loads(f.read())

    return data

################################################################################################################
################################################################################################################
#   _                    _     _                 ____             _ _       
#  | |    ___   __ _  __| |   | |___  ___  _ __ / ___| _ __  _ __(_) |_ ___ 
#  | |   / _ \ / _` |/ _` |_  | / __|/ _ \| '_ \\___ \| '_ \| '__| | __/ _ \
#  | |__| (_) | (_| | (_| | |_| \__ \ (_) | | | |___) | |_) | |  | | ||  __/
#  |_____\___/ \__,_|\__,_|\___/|___/\___/|_| |_|____/| .__/|_|  |_|\__\___|
#                                                     |_|                                                                                                                                             
                                                              
def  loadSpriteImages(path):
    """ Load sprite images into either a dictionary of moves or a list of images depending
        on whether the "sprite" is a multi move character or a single effect with just frames
        to play.

        This method reads a json file looking for the following formats (right now):

    """

    if not os.path.isfile(os.path.join(path,"moves.json")):
        print(f"Error: 'moves.json' is required to be in folder: {path}!")
        sys.exit()


    # make raw string into a python dictionary 
    sprite_info = loadJsonSprite(path,"moves.json")

    # base name is used to build filename
    base_name = sprite_info['base_name']

    # ext as well
    ext = sprite_info['ext']

    # If moves is a key in the dictionary then we create a dictionary of
    # of moves where each move points to a list of images for that move
    if 'moves' in sprite_info:
        moves = {}

        for move,info in sprite_info['moves'].items():
            moves[move] = []

            if type(info) == list:
                for num in info:
                    moves[move].append(os.path.join(path,base_name+num+ext))
            else:
                for num in info['frames']:
                    moves[move].append(os.path.join(path,base_name+num+ext))
        
        return moves

    # If frames in the dictionary, then its an effect with a list of images
    # for that effect. We need to order them before return since glob
    # doesn't get directory items in order. 
    elif 'frames' in sprite_info:
        images = sprite_info['frames']
        
        if type(images) == list:
            pass
        elif type(images) == str and images == '*':
            images = glob.glob(os.path.join(path,'*'+ext))
            images.sort()
            return images

    else:
        print(f"Error: 'moves' or 'frames' key not in json!!")
        sys.exit()

################################################################################################################
################################################################################################################
#       _             _       _     _   ____  _     _                       
#   ___| |_ _ __ __ _(_) __ _| |__ | |_|  _ \(_)___| |_ __ _ _ __   ___ ___ 
#  / __| __| '__/ _` | |/ _` | '_ \| __| | | | / __| __/ _` | '_ \ / __/ _ \
#  \__ \ |_| | | (_| | | (_| | | | | |_| |_| | \__ \ || (_| | | | | (_|  __/
#  |___/\__|_|  \__,_|_|\__, |_| |_|\__|____/|_|___/\__\__,_|_| |_|\___\___|
#                       |___/                                                          
                                                              

def straightDistance(A,B,C=None,D=None):
    '''
    Returns the cartisian distance between 2 points on a 2d plane.

            Parameters:
                    A (int): x coord of point 1
                    B (int): y coord of point 1
                    C (int): x coord of point 2
                    D (int): y coord of point 2

            Returns:
                    distance (float): Cartesian distance
    '''
    if type(A) == tuple and type(B) == tuple:
        distance = ((A[0]-B[0])**2 + (A[1]-B[1])**2)**0.5
    else:
        distance = ((A-C)**2 + (B-D)**2)**0.5
    return distance

def taxiCabDistance(xA,yA,xB,yB):
    '''
    Returns the manhatten or taxi_cab distance between 2 points on a 2d grid.

            Parameters:
                    x1 (int): x coord of point 1
                    y1 (int): y coord of point 1
                    x2 (int): x coord of point 2
                    y2 (int): y coord of point 2

            Returns:
                    distance (float): Manhatten or taxicab  distance
    '''
    distance = abs(xA-xB) + abs(yA-yB)
    return distance

################################################################################################################
################################################################################################################
#                  _  __                            
#   _ __ ___  _   _| |/ /_      ____ _ _ __ __ _ ___ 
#  | '_ ` _ \| | | | ' /\ \ /\ / / _` | '__/ _` / __|
#  | | | | | | |_| | . \ \ V  V / (_| | | | (_| \__ \
#  |_| |_| |_|\__, |_|\_\ \_/\_/ \__,_|_|  \__, |___/
#             |___/                        |___/     
                                                                            

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
            kargs[key] = val
        else:
            args.append(arg)
    return args,kargs

################################################################################################################
################################################################################################################
#    ____      _            _____                 _   _                 
#   / ___|___ | | ___  _ __|  ___|   _ _ __   ___| |_(_) ___  _ __  ___ 
#  | |   / _ \| |/ _ \| '__| |_ | | | | '_ \ / __| __| |/ _ \| '_ \/ __|
#  | |__| (_) | | (_) | |  |  _|| |_| | | | | (__| |_| | (_) | | | \__ \
#   \____\___/|_|\___/|_|  |_|   \__,_|_| |_|\___|\__|_|\___/|_| |_|___/
                                                                      

def loadColors(infile):
    '''
    Loads a json color file into a python dictionary.
        Params:
            infile (string) : path to json input file
        Returns:
            colors (dictionary) : dictionary of colors (hex and rgb)
    '''
    with open(infile,'r') as f:
        data = f.read()
        colors = json.loads(data)
    return colors

def rgbColors(infile):
    '''
    Loads a json color file into a python dictionary.
        Params:
            infile (string) : path to json input file
        Returns:
            colors (dictionary) : dictionary of colors (rgb only)
    '''
    rgb = {}
    with open(infile,'r') as f:
        data = f.read()
        colors = json.loads(data)
    for key,color in colors.items():
        rgb[key] = color['rgb']
    return rgb

################################################################################################################
################################################################################################################

cardinal_directions = ('W','NW','N','NE','E','SE','S','SW')

def getCardinalDirection(origin,target):
    """
    https://gamedev.stackexchange.com/questions/49290/whats-the-best-way-of-transforming-a-2d-vector-into-the-closest-8-way-compass-d

    This method finds the angle between an origin location and a target location.
    Using some simple but cool arithmetic, it converts the angle into an int value: 0-7 (8 values) that corresponds
        to one of the 8 semi-major cardinal directions. Major being N, S, E, and W. Each of the 8 represents a 45 degree
        pie slice of the compass circle.
            Params:
                origin: (tuple): (x,y)
                target: (tuple): (x,y)
            Returns:
                cardinal_direction (string) : one of 'W','NW','N','NE','E','SE','S','SW'
    """
    cards = []
    dx = origin[0] - target[0]
    dy = origin[1] - target[1]
    angle = math.atan2(dy, dx)

    octant = round(8 * angle / (2*math.pi) + 8) % 8

    return cardinal_directions[octant]

################################################################################################################
################################################################################################################
#               _       _   ___       ____           _   
#   _ __   ___ (_)_ __ | |_|_ _|_ __ |  _ \ ___  ___| |_ 
#  | '_ \ / _ \| | '_ \| __|| || '_ \| |_) / _ \/ __| __|
#  | |_) | (_) | | | | | |_ | || | | |  _ <  __/ (__| |_ 
#  | .__/ \___/|_|_| |_|\__|___|_| |_|_| \_\___|\___|\__|
#  |_|                                                   
def pointInRect(p,rect):
    """ Point Insice Rectangle
        Params:
            p <tuple>       : point (x,y)
            rect <tuple>    : rectangle (x,y,w,h)
        Returns:
            bool            : is the point inside the rectabgle (on the edge is not in)
                              But we could change the '<' to '<=' and then it would be testing
                              for inside OR touching. Seems silly, but some int the spatial world
                              would argue big difference (I wouldn't)
    """
    return rect[0] < p[0] < rect[0] + rect[2] and rect[1] < p[1] < rect[1] + rect[3]
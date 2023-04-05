import sys
import json
import math


def straightDistance(A, B, C=None, D=None):
    """
    Returns the cartisian distance between 2 points on a 2d plane.

            Parameters:
                    A (int): x coord of point 1
                    B (int): y coord of point 1
                    C (int): x coord of point 2
                    D (int): y coord of point 2

            Returns:
                    distance (float): Cartesian distance
    """
    if type(A) == tuple and type(B) == tuple:
        distance = ((A[0] - B[0]) ** 2 + (A[1] - B[1]) ** 2) ** 0.5
    else:
        distance = ((A - C) ** 2 + (B - D) ** 2) ** 0.5
    return distance


def taxicabDistance(xA, yA, xB, yB):
    """
    Returns the manhatten or taxi_cab distance between 2 points on a 2d grid.

            Parameters:
                    x1 (int): x coord of point 1
                    y1 (int): y coord of point 1
                    x2 (int): x coord of point 2
                    y2 (int): y coord of point 2

            Returns:
                    distance (float): Manhatten or taxicab  distance
    """
    distance = abs(xA - xB) + abs(yA - yB)
    return distance


def manhattanDistance(A, B, C=None, D=None):
    """
    Returns the manhatten or taxi_cab distance between 2 points on a 2d grid.

            Parameters:
                    A (tuple): xy of first point
                    B (tuple): xy of second point

                            OR
            Parameters:
                    A (int): x coord of point 1
                    B (int): y coord of point 1
                    C (int): x coord of point 2
                    D (int): y coord of point 2

            Returns:
                    distance (float): Manhattan or taxicab  distance
    """
    if type(A) == tuple and type(B) == tuple:
        xA = A[0]
        yA = A[1]
        xB = B[0]
        yB = B[1]
    else:
        xA = A
        yB = B
        xB = C
        yB = D

    distance = abs(xA - xB) + abs(yA - yB)
    return distance


def mykwargs(argv):
    """
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
    """
    args = []
    kargs = {}

    for arg in argv:
        if "=" in arg:
            key, val = arg.split("=")
            kargs[key] = val
        else:
            args.append(arg)
    return args, kargs


def load_colors(infile):
    """
    Loads a json color file into a python dictionary.
        Params:
            infile (string) : path to json input file
        Returns:
            colors (dictionary) : dictionary of colors (hex and rgb)
    """
    with open(infile, "r") as f:
        data = f.read()
        colors = json.loads(data)
    return colors


def rgb_colors(infile):
    """
    Loads a json color file into a python dictionary.
        Params:
            infile (string) : path to json input file
        Returns:
            colors (dictionary) : dictionary of colors (rgb only)
    """
    rgb = {}
    with open(infile, "r") as f:
        data = f.read()
        colors = json.loads(data)
    for key, color in colors.items():
        rgb[key] = color["rgb"]
    return rgb


cardinal_directions = ("W", "NW", "N", "NE", "E", "SE", "S", "SW")


def getCardinalDirection(origin, target):
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
    # dx = origin[0] - target[0]
    # dy = origin[1] - target[1]
    dx = target[0] - origin[0]
    dy = target[1] - origin[1]
    angle = math.atan2(dy, dx)

    octant = round(8 * angle / (2 * math.pi) + 8) % 8

    return cardinal_directions[octant]


class Logg:
    """
    Simple little logger clas to help with debugging
    """

    def __init__(self):
        self.logfile = open("logger.txt", "w")

    def log(self, stuff):
        self.logfile.write(stuff + "\n")


class EventContainer:
    """Dictionary of events all kept in one place for use in other classes.
    Not sure on "best practices" or performance, but this lets me pass
    all the events to any class or function that needs em.
    """

    def __init__(self):
        self.events = {
            "keydown": None,
            "keyup": None,
            "mouse_motion": None,
            "mouse_button_up": None,
            "all_pressed": None,
        }

    def reset(self):
        """Set all to None"""
        for k, v in self.events.items():
            self.events[k] = None

    def __str__(self):
        """Dump instance to screen or wherever"""
        s = ""
        for k, v in self.events.items():
            if k == "all_pressed":
                continue
            s += f"{k} : {v}\n"

        return s

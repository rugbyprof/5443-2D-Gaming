

######################################################################################################################################################
######################################################################################################################################################
##  ██████╗ ██╗      █████╗ ████████╗███████╗ ██████╗ ██████╗ ███╗   ███╗ ██████╗ ███████╗███╗   ██╗███████╗██████╗  █████╗ ████████╗ ██████╗ ██████╗ 
##  ██╔══██╗██║     ██╔══██╗╚══██╔══╝██╔════╝██╔═══██╗██╔══██╗████╗ ████║██╔════╝ ██╔════╝████╗  ██║██╔════╝██╔══██╗██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗
##  ██████╔╝██║     ███████║   ██║   █████╗  ██║   ██║██████╔╝██╔████╔██║██║  ███╗█████╗  ██╔██╗ ██║█████╗  ██████╔╝███████║   ██║   ██║   ██║██████╔╝
##  ██╔═══╝ ██║     ██╔══██║   ██║   ██╔══╝  ██║   ██║██╔══██╗██║╚██╔╝██║██║   ██║██╔══╝  ██║╚██╗██║██╔══╝  ██╔══██╗██╔══██║   ██║   ██║   ██║██╔══██╗
##  ██║     ███████╗██║  ██║   ██║   ██║     ╚██████╔╝██║  ██║██║ ╚═╝ ██║╚██████╔╝███████╗██║ ╚████║███████╗██║  ██║██║  ██║   ██║   ╚██████╔╝██║  ██║
##  ╚═╝     ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
"""
PlatformGenerator

Description:
    This class generates a platform level based on many rolls of the dice. It has over
    20 parameters that you could tweak, but don't need to. Its not perfect, but I had
    to let it go and not fix some of the issues (see Todo).

    Its important to note that (see example output below) each character printed represents a possible tile. 
    I printed lines instead of blanks for readability and I used the following number scheme:
        0       = floor 
        1 - N   = layer of platforms

    So the EXAMPLE below has a blocky floor (all the zeros) and three levels of platforms.
    There are two "pits" in the floor and a total of 6 platforms to jump on. 

                                EXAMPLE:
                                ___________33333______________
                                ______________________________
                                __22222222_________22222______
                                ______________________________
                                _1111111_______1111______1111_
                                ______________________________
                                __________0000000_____00000000
                                __________0000000_____00000000
                                __________0000000_____00000000
                                00000_____000000000___00000000

    This is important because each "character" is equivalent to 1 tile, where a tile could be anywhere from 16x16
    pixels to 128x128 pixels. This output assumes equal tile sizes all the way around, where in some tile sets
    a few tiles may take up multiple slots. Anyway, most tile sets have integer values associated with each tile
    and you could "assign" specific tile numbers to different portions of your generated platform screen. Below
    we could assume: 0 = rock (or ground) 1 and 2 = platform types and maybe 3 is a cloud! Its up to you. 

    I mention that 1 Tile = 1 character because the important params right below are what you will change to configure
    your platform. So remember a 50x20 matrix results in a 1250px x 500px background for a tile size of 25x25. 

Params:
    Important Ones:
        rows            <int>  : y tiles high
        cols            <int>  : x tiles wide
        levels          <int>  : the number of platform levels desired
        platforms_per   <int>  : the number of platforms per level 

    Params:
        floor_median                <int>   : An integer value is generated, then the next two params are based on this median value.
        floor_max_height            <int>   : Some integer greater than the median
        floor_min_height            <int>   : Some integer less than the median

                                    The previous 3 vars gives us variable floor height with some consistancy, and lets us control how drastic
                                    the changes are between heights. 

        floor_max_width             <int>   : max cols a floor segment can be
        floor_min_width             <int>   : min cols a floor segment can be

                                    The smaller the min value the shorter and choppier the floor can become. 
                                    The bigger the max value the wider a segment could become creating long flat regions (ok if this is what you want)

        floor_platform_buffer       <int>   : empty rows between tallest floor and first level of platforms


        pit_max_width               <int>   : max cols a pit segment can be
        pit_min_width               <int>   : min cols a pit segment can be

                                    Controls variations in pit size.

        pit_chance                  <int>: value between 0-100 30 is default

                                    Higher the value, the more pits generated.

        pit_max_consecutive         <int>   : max pits in a row (otherwise pit could get huge)

                                    Depends  on preference, but I assumed that most don't want a bunch of pits 
                                    generated back to back since a character may not be able to jump over. 

        platform_max_width          <int>   : max width of a platform
        platform_min_width          <int>   : min width of a platform 

                                    Variation in generated platform size

        platform_layer_min_height   <int>   : spaces out platforms vertically
        platform_layer_max_height   <int>   : adds leeway to put platforms within a layer

                                    I made each platform layer (level) have a variance in height hoping
                                    it would be aesthetically pleasing

        platform_min_gap            <int>   : gap between platforms (left to right)
        platform_max_gap            <int>   : max gap between platforms

                                    Space between platforms within layers.
    

TODO:
    1) Fix the issue with generating platforms in the same subset of columns. Meaning two platforms could be stacked on each other.
       Here is a small example. Notice the 2's over the 1's. It doesn't always happen, but needs fixed.

            BAD:                                          BETTER:
                ______________________________              ___________33333______________
                ______________________________              ______________________________
                __22222222___22222222_________              __22222222_________22222______
                _1111111_______1111______1111_              ______________________________
                ______________________________              _1111111_______1111______1111_
                ______________________________              ______________________________
                __________0000000_____00000000              __________0000000_____00000000
                __________0000000_____00000000              __________0000000_____00000000
                __________0000000_____00000000              __________0000000_____00000000
                00000_____000000000___00000000              00000_____000000000___00000000

    2) TEST each parameter to make sure all my parameters do as advertised (I'm positive they don't)! But it is a working base model.
"""
import random
import os
import sys

class PlatFormGenerator(object):
    """
    PlatFormGenerator data members:
        rows                        <int>   : number of rows in level
        cols                        <int>   : number of cols in level
        floor_median                <int>   : min and max floor height based on this value
        floor_max_height            <int>   : number of rows above median
        floor_min_height            <int>   : number of rows below median
        floor_max_width             <int>   : max cols a floor segment can be
        floor_min_width             <int>   : min cols a floor segment can be
        floor_platform_buffer       <int>   : empty rows between tallest floor and first level of platforms
        pit_max_width               <int>   : max cols a pit segment can be
        pit_min_width               <int>   : min cols a pit segment can be
        pit_chance                  <int>   : value between 0-100 30 is default
        pit_max_consecutive         <int>   : max pits in a row (otherwise pit could get huge)
        platform_max_width          <int>   : max width of a platform
        platform_min_width          <int>   : min width of a platform 
        platform_layer_min_height   <int>   : spaces out platforms vertically
        platform_layer_max_height   <int>   : adds leeway to put platforms within a layer
        platform_min_gap            <int>   : gap between platforms (left to right)
        platform_max_gap            <int>   : max gap between platforms
    """
    def __init__(self,**kwargs):

        

        self.rows = kwargs.get('rows',40)
        self.cols = kwargs.get('cols',80)
        self.floor_median =  kwargs.get('floor_median',int(self.rows*.2)) ##  default is 10% of total height
        self.floor_max_height = kwargs.get('floor_max_height',self.floor_median+3)
        self.floor_min_height = kwargs.get('floor_min_height',self.floor_median-3)
        self.floor_max_width = kwargs.get('floor_max_width',10)
        self.floor_min_width = kwargs.get('floor_min_width',3)
        self.floor_platform_buffer = kwargs.get('floor_platform_buffer',3)
        self.pit_max_width = kwargs.get('pit_max_width',6)
        self.pit_min_width = kwargs.get('pit_min_width',2)
        self.pit_chance = kwargs.get('pit_chance',30)
        self.pit_max_consecutive = kwargs.get('pit_max_consecutive',3)
        self.platform_max_width = kwargs.get('platform_max_width',10)
        self.platform_min_width = kwargs.get('platform_min_width',3)
        self.platform_layer_min_height = kwargs.get('platform_layer_min_height',2)
        self.platform_layer_max_height = kwargs.get('platform_layer_max_height',7)
        self.platform_min_gap = kwargs.get('platform_min_gap',3)
        self.platform_max_gap = kwargs.get('platform_max_gap',7)
        self.tile_size = 1  ##  does nothing but could be added as a multiplier of sorts 

        self.tallest_floor = 0      ##  init tallest floor to zero
        self.matrix = []            ##  2d matrix to hold our level      

        self.levels = kwargs.get('levels',0)
        self.platforms_per = kwargs.get('platforms_per',0)

        for r in range(int(self.rows)):
            self.matrix.append(['..' for x in range(self.cols)])

        self.generateFloor()
        self.generatePlatforms(self.levels,self.platforms_per)
        #self.generatePlatforms()
        

    def generateFloor(self):
        """ Generates a floor with pits for a platformer level
        """
        startx = 0              ##  starting x coord (zero always)
        endx = self.cols        ##  ending x coord (width of matrix)
        num_pits = 0            ##  count how many pits created (so we can limit)
        consecutive_pits = 0    ##  consecutive pits get real big, se we track them

        ##  add a floor chunk to the far bottom left of the level
        ##  so we always have a place to enter
        width,height = self.generateFloorChunk()
        self.addToMatrix('floor',width,height,startx,0,0)
        startx += width

        ##  add a floor chunk to the far bottom right of the level
        ##  so we can always leave
        width,height = self.generateFloorChunk()
        self.addToMatrix('floor',width,height,endx-width,0,0)
        endx -= width

        ##  keep moving startx over as we generate chunks and pits until
        ##  it gets to the end
        while startx < endx:
            
            ##  if have too many pits next to each other, add a floor block
            ##  otherwise, roll the dice to see if we make a pit
            if consecutive_pits <= self.pit_max_consecutive and random.random() * 100 < self.pit_chance:
                
                ##  make a pit (really generate a width and add it to startx)
                width = self.generatePit()
                if startx + width >= endx:
                    ##  we have reached the far right of the floor
                    break

                self.addToMatrix('pit',width,height,startx,0,0)

                startx += width         ##  move startx over to the right
                num_pits += 1           ##  count pits made
                consecutive_pits += 1   ##  count consecutive pits

            else:
                ##  make a floor chunk

                ##  reset consecutive pits (cause this aint no pit)
                consecutive_pits = 0

                ##  generate a chunk
                width,height = self.generateFloorChunk()

                ##  if were close to the end, just add more to the width to finish 
                if startx + width >= endx:
                    width = endx - startx
                
                ##  adds to our matrix wich will be turned into our level
                self.addToMatrix('floor',width,height,startx,0,0)

                startx += width

    def roll_dice(self,start,stop):
        """ roll the dice! Facade pattern for random.randrange. It just reads better.
            Params:
                start <int> : low value
                stop <int> : high value
            Returns:
                int between low and high (inclusive? can't rememember)
        """
        return int(random.randrange(start,stop))

    def calculateLevelLocations(self,levels=0):
        """ Determine how many levels will fit in this matrix size.
            Params:
                levels <int> : choose number of levels, 0 = as many as will fit
                               based on the random nums generated.
        """
        layers = {} ##  layers dict holds info about platform layers (height, and starting y coord)

        layer = 0   #  index for keeping track of current layer

        currenty  = self.tallest_floor + self.floor_platform_buffer     # just above tallest floor

        # levels == 0 means generate all that will fit.
        if levels == 0:

            # while there is room for another layer
            # rows-2 gives a little breathing room
            while currenty < self.rows-2:

                # get a random height between layer_height params
                height = self.roll_dice(self.platform_layer_min_height,self.platform_layer_max_height)

                # save that value as a dict in the layers dict using "layer" as a key
                layers[layer] = {"y":currenty,"height":height}

                # create another layer (next int key)
                layer += 1

                # if we have enough ... get out!
                if layer >= levels:
                    break

                # move currenty up toward top of level
                currenty += height

        else: # we have a specific number of levels

            # currenty is just above floor
            # table_height - currenty divided by levels should
            # give us as many as can fit
            sizey = (self.rows - currenty) // levels

            # build our layers dict with the y location of the layer
            # and its consistent sizey (probably should be more random).
            for layer in range(int(levels)):
                layers[layer] = {"y":currenty,"height":sizey}

                # move toward top of level
                currenty += sizey

        return layers

    def generatePlatforms(self,levels=0,platforms_per=0):
        """ Generate platforms for our platformer game. 
            Params:
                levels          <int> :  choose number of platform levels. 
                                         0 = as many as can fit based on the random nums
                platforms_per   <int> :  Number of platforms per level. 
                                         Not defined will result in random number based on width of game.
            
        """
        layers = self.calculateLevelLocations(levels)   ##  get the generated layers
        layers_keys =  list(layers.keys())              ##  keys to the layers dict so I can randomly pick layers easier
        startx = 2                                      ##  start at x coord 2 (maybe add to config?)
        endx = self.cols                                ##  set ending x coord to entire width of level


        # if platforms_per is zero, generate as many as will fit
        if platforms_per == 0:

            # start with key = 0
            # k is used as an index into the layers dictionary to pull out
            # the layer info (y location, and height)
            k = 0

            # step through each layer from calculateLevelLocations
            while k <= len(layers_keys)-1:

                # start somewhere between x=1 and x=5 to create a platform
                startx = self.roll_dice(1,5)

                # while we haven't gone over the left of the matrix
                while startx < self.cols:
                    
                    # y is a random value between the 'y' (bottom of the layer) and the layers 'height'
                    y = self.roll_dice(layers[k]['y'],layers[k]['y']+layers[k]['height'])

                    
                    platform_width = self.roll_dice(self.platform_min_width,self.platform_max_width)
                    if startx + platform_width > self.cols:
                        k += 1

                        break
                    self.addToMatrix('platform',platform_width,1,startx,y,k+1)
                    startx = startx + platform_width + self.roll_dice(self.platform_min_gap,self.platform_max_gap)
        else:
            # creates a list of zeros which allows me to keep track of the platform count
            # for each layer (using k as an index)
            platform_count = [0 for x in range(len(layers))]    

            # as long as ALL the platforms created is less than how many we want per layer 
            # times how many layers. We may get a lot on one, and a few on another, but thats
            # what randomization is about
            while sum(platform_count) < platforms_per * len(layers):
                k = random.choice(layers_keys)                                          # get a random index from layers 
                y = self.roll_dice(layers[k]['y'],layers[k]['y']+layers[k]['height'])   # generate a random height between 
                platform_width = self.roll_dice(self.platform_min_width,self.platform_max_width)

                # does our new platform go beyond right of matrix?
                if startx + platform_width > self.cols:

                    # if so, go back to colums 1-5
                    startx = self.roll_dice(1,5)

                ##  while self.columnsTaken(startx,startx+platform_width,platform_width) > .5:
                ##      print(f"k={k} {self.columnsTaken(startx,startx+platform_width,platform_width)}")
                ##      startx += (platform_width // 2)
                
                # save it to our level matrix
                self.addToMatrix('platform',platform_width,1,startx,y,'10')

                # increment this layers count
                platform_count[k] += 1

                # get a new starting position (not sure about this)
                startx = (startx + platform_width + self.roll_dice(self.platform_min_gap,self.platform_max_gap)) % self.cols

        self.printMatrix()

    def columnsTaken(self,startx,endx,platform_width):
        """ Counts the number of columns in the matrix that are occupied. We don't 
            want to stack platforms directly on top of each other.
            Params:
                startx <int> : starting x coord
                endx <int> : ending x coord
                platform_width <int> : platform width
        """
        y = self.tallest_floor + self.floor_platform_buffer
        count = 0

        for i in range(startx,endx):
            for j in range(y,self.rows):
                if self.matrix[j][i] != '.':
                    count += 1

        return round(count / platform_width,2)

    def generateFloorChunk(self):
        """ Generates width and height between configured min's and max's
            Params:
                None
            Returns:
                tuple (width,height)
        """
        width =  self.roll_dice(self.floor_min_width,self.floor_max_width)
        height = self.roll_dice(self.floor_min_height,self.floor_max_height)

        ##  keep track so we can generate lowest level above this tall floor
        if height  > self.tallest_floor:
            self.tallest_floor = height 

        return(width,height)
    
    def generatePit(self):
        """ Generates width of a pit (really rand num between two values)
            Params:
                None
            Returns:
                int
        """
        
        return self.roll_dice(self.pit_min_width,self.pit_max_width)

    def pad_str(self,s,d):
        s = str(s)
        return s.zfill(d)

    def addToMatrix(self,block_type,width,height,startx,starty=0,tile_type=1):
        """ Adds a generated construct to our current platform level
            Params:
                block_type <enum> : 'floor' or 'platform'
                width       <int> : width of chunk
                height      <int> : height of chunk
                startx       <int> : starting x coord where to write
                tile_type   <int> : can be used for tile maps
            Returns:
                None
        """
        if not block_type in ['floor','platform','pit']:
            print(f"Error: block_type must be 'floor' or 'platform' not {block_type}!")
            sys.exit()


        # bloated temp fix
        endx = startx+width
        if block_type == 'platform':
            rows = range(starty-1,starty)
            
            for i in rows:
                for j in range(startx,endx):
                    if j == startx:
                        self.matrix[i][j] = '13'
                    elif j == endx-1:
                        self.matrix[i][j] = '15'
                    else:
                        self.matrix[i][j] = '14'

        elif block_type == 'floor':
            # we do floor (dirt) tiles

            # bottom of floor chunk
            self.matrix[0][startx] ='12'        # bottom left floor
            for j in range(startx+1,endx-1):
                self.matrix[0][j] = '09'        # bottom mid floor
            self.matrix[0][endx-1] ='16'        # bottom right floor

            # middle of floor chunk
            rows = range(1,height-1)
            for i in rows:
                self.matrix[i][startx] = '04'       # mid left
                for j in range(startx+1,endx-1):
                    self.matrix[i][j] = '05'        # mid mid
                self.matrix[i][endx-1] = '06'       # mid left

            # top of floor chunk
            self.matrix[height-1][startx] ='01'         # top left floor
            for j in range(startx+1,endx-1):
                self.matrix[height-1][j] = '02'        # top mid floor
            self.matrix[height-1][endx-1] ='03'        # top right floor

        elif block_type == 'pit':
            rows = range(0,height-1)
            for i in rows:
                for j in range(startx,endx):
                    self.matrix[i][j] = '18'
            for j in range(startx,endx):
                self.matrix[height-1][j] = '17'
        else:
            # not sure what type it is
            for i in rows:
                for j in range(startx,endx):
                    self.matrix[i][j] = self.pad_str(tile_type,2)

    def printMatrix(self):
        for row in reversed(self.matrix):
            for col in row:
                sys.stdout.write(str(col))
            sys.stdout.write("\n")

    def saveMatrix(self,fout='platform.map'):
        f = open(fout,'w')
        for row in reversed(self.matrix):
            for col in row:
                f.write(str(col))
            f.write("\n")


################################################################################################################
################################################################################################################
##  ███╗   ███╗██╗   ██╗     ██╗  ██╗██╗    ██╗ █████╗ ██████╗  ██████╗ ███████╗
##  ████╗ ████║╚██╗ ██╔╝     ██║ ██╔╝██║    ██║██╔══██╗██╔══██╗██╔════╝ ██╔════╝
##  ██╔████╔██║ ╚████╔╝█████╗█████╔╝ ██║ █╗ ██║███████║██████╔╝██║  ███╗███████╗
##  ██║╚██╔╝██║  ╚██╔╝ ╚════╝██╔═██╗ ██║███╗██║██╔══██║██╔══██╗██║   ██║╚════██║
##  ██║ ╚═╝ ██║   ██║        ██║  ██╗╚███╔███╔╝██║  ██║██║  ██║╚██████╔╝███████║
##  ╚═╝     ╚═╝   ╚═╝        ╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝
                                                                            

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
    print("")
    print(wrap("Minimum Example:"))
    print(wrap("    python platformGenerator.py rows=N cols=N\n"))
    print(wrap("Extended Example:"))
    print(wrap("    python platformGenerator.py rows=N cols=N levels=N platform_per=N\n"))
    print("All Available Params:")
    print(PlatFormGenerator.__doc__)
    print("")
    print("Use any of the above params to configure a run, simply pass them in on the command line:\n")
    print("    python platformGenerator.py param1_name=value1 param2_name=value2 paramN_name=valueN\n")
    print(line('*'))

    sys.exit()

  

################################################################################################################
################################################################################################################
##  ███╗   ███╗ █████╗ ██╗███╗   ██╗
##  ████╗ ████║██╔══██╗██║████╗  ██║
##  ██╔████╔██║███████║██║██╔██╗ ██║
##  ██║╚██╔╝██║██╔══██║██║██║╚██╗██║
##  ██║ ╚═╝ ██║██║  ██║██║██║ ╚████║
##  ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝

if __name__=='__main__':


    required_params = 2 
    argv = sys.argv[1:] # strip file name (platformGenerator.py) out of args

    # print usage if not called correctly
    if len(argv) < required_params:
        usage()

    # get processed command line args
    args,kwargs = myKwargs(argv)

    # send them to generator
    p = PlatFormGenerator(**kwargs)
    p.saveMatrix()

    

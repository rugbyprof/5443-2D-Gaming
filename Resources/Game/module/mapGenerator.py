"""
"""
import os
import sys
import json
import time
from PIL import Image

from helper_functions import loadJson

class MapLoader(object):
    def __init__(self,**kwargs):
        path = kwargs.get('path',None)
        self.ids = {}

        if not path:
            print("Error: need a path to a map!!")
            sys.exit()

        self.data = loadJson(path)
        self.gen_ids()

    def get(self,key,subkey):
        return self.data[key][subkey]

    def get_tile_by_id(self,id):
        for k,v in self.ids.items():
            for kk,vv in v.items():
                if id == vv:
                    return self.data[k][kk]

    def dump(self):
        print(self.data)
        
    def get_id(self,key,subkey):
        """ get numeric id based on key and subkey
        """
        return self.ids[key][subkey]

    def pad_str(self,s,d):
        s = str(s)
        return s.zfill(d)


    def gen_ids(self,out=False):
        """ generate the unique integer ids for each tile
        """
        i = 0
        for k,v in self.data.items():
            self.ids[k] = {}

            if out:
                print(f"{k}")
            for kk,vv in v.items():
                self.ids[k][kk] = self.pad_str(i,2)
                if out:
                    print(f"    {kk} = {i}")
                i += 1
            
    def createPlatformSheet(self,**kwargs):
        """ Takes a sprite sheet thats layed out in a consistent manor (same size tiles), 
            it will take each "tile" and create a seperate image. 
            Params:
                map_path <string>     : path to input map
                outpath <string>    : path to outinput folder
                rows <int>          : how many rows in the sheet
                cols <int>          : how many columns in the sheet
                frame_width <int>   : width of frame in pixels
                frame_height <int>  : height of frame in pixels
                direction <xy / yx> : process row then col (xy) or column then row (yx)
                image_type <string> : default png 
        """
        map_path = kwargs.get("map_path",None)
        save_path = kwargs.get("save_path",None)
        image_type = kwargs.get("image_type","png")
        tile_size = kwargs.get("tile_size",25)

        # get unique timestamp for outfile name
        ts = time.time()
        ts = int(ts)

        if save_path == None:
            save_path = os.path.join('platform_sheet_'+str(ts)+'.png')
        else:
            if save_path[-3:] != image_type:
                save_path = os.path.join(save_path,'platform_sheet_'+str(ts)+'.png')

        if not os.path.isfile(map_path):
            print(f"Error: {map_path} is not a proper file! ")
            sys.exit()

        with open(map_path,"r") as f:
            map_data = f.read()

        map_data = map_data.split("\n")

        
        height = len(map_data) * tile_size
        width = len(map_data[0])//2 * tile_size

        print(width,height)

        # open the sprite sheet
        tiles = Image.open("./images/lush_green_map.png")
        background = Image.open("./images/lush_green_background.png")
        background = background.resize((width,height))

        # # create a blank image to "paste" on
        map_img = Image.new('RGBA', (width, height),(255, 255, 255, 0))

        buffer = 4

        row = 0
        for line in map_data:
            col = 0
            for i in range(0,len(line),2):
                id = line[i]+line[i+1]
                if not '.' in id:
                    c = self.get_tile_by_id(id)
                    print(c)
                    # {'x': 432, 'y': 114, 'w': 95, 'h': 95}
                    tile = tiles.crop((c['x']+buffer, c['y']+buffer, c['x']+c['w']-buffer, c['y']+c['h']-buffer))
                    tile = tile.resize((tile_size,tile_size)) 
                    tile.save("./images/tiles/"+str(id)+'_'+str(row)+str(col)+".png", quality=95)
                    background.paste(tile, (col*tile_size, row*tile_size),tile)
                col += 1
            row += 1
        background.save("./images/generated_map.png", quality=95)


if __name__=='__main__':
    m = MapLoader(path='./data/lush_green_map.json')
    m.createPlatformSheet(map_path="platform.map")
    # m.keys()
    # m.dump()
    # print(m.get("floor","top_right"))
    # print(m.get_id("floor","top_right"))

    print(m.get_tile_by_id('11'))

## Program: spriter.py

### Extract: 

Extracting will take a sprite sheet (basic one) with consistent size frames and turn it into a directory of individual images. It assumes a table format (rows and columns). The link below points to a pacman sprite sheet with 9 rows and 17 columns. However columns 13-17 are used for a single sprite with nothing below row 1. 

<img src="https://cs.msutexas.edu/~griffin/zcloud/zcloud-files/pacman_ghosts.png" width="340">


>This script doesn't handle URL's, so you would need to copy whatever image you use to your local file system. I could adapt it, but I won't

**Example 1:**  extract all the images (including a bunch of blank ones at the end)

```bash        
python spriter.py action=extract inpath=pacman_ghosts.png outpath=pacman_ghosts_folder name=pacman_images rows=9 cols=17 frame_width=40 frame_height=40 direction=xy
```

This wouldn't much good if you wanted to seperate each color of the pacman sheet. See following...
    
**Example 2:** extract blue pacman. Uses same command as above but only reads three columns  and starts with an xoffset of 360 (skipping red, pink, and orange)

```bash        
python spriter.py action=extract inpath=pacman_ghosts.png outpath=pacman_bluefolder name=pacman_blue rows=9 cols=3 frame_width=40 frame_height=40 direction=xy xoffset=120
```

<img src="https://cs.msutexas.edu/~griffin/zcloud/zcloud-files/pacman_spritesheet_xydir.png" width="60" >

Example 3: extract ghost dying

```bash        
python spriter.py action=extract inpath=pacman_ghosts.png outpath=pacman_ghosts_foldername=pacman_pink rows=1 cols=5 frame_width=40 frame_height=40 direction=xy xoffset=480
```

<img src="https://cs.msutexas.edu/~griffin/zcloud/zcloud-files/pacman_spritesheet_die.png"  width="100">


### Create:

Creating a spritesheet takes a folder of images and processes them based on their alphanumeric order.  You tell the script how many rows and columns you want and a frame size, and it will put all images in the folder on a single image sheet in order (row wise or column wise). 

**Example:**
    
If you have the orange pacman in a folder number orange_001.png orange_002.png ... all the way to orange_027.png and they are ordered like the top 3 orange sprites are 1-3 and the bottom row  of orange is 25-27, then you could re-create a sprite sheet just for orange (using your images) like this:
        
```bash
python spriter.py action=create inpath=pacman_ghosts_folder [outpath=pacman_ghosts_folder] name=pacman_orange_sprite.png rows=9 cols=3 frame_width=40 frame_height=40 direction=xy
```

<img src="https://cs.msutexas.edu/~griffin/zcloud/zcloud-files/pacman_spritesheet_xydir.png" width="60" >

If you swap xy => yx this is what you get:

<img src="https://cs.msutexas.edu/~griffin/zcloud/zcloud-files/pacman_spritesheet_yxdir.png" width="60" >

If you don't provide an out path it will assume same directory as in path and call the new file sprite_sheet_`timestamp`.png  where timestamp is an integer value representing the time it was made.



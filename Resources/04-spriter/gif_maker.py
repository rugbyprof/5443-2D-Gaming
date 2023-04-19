from PIL import Image
import os, sys


class SpriteSheetExtractor:
    def __init__(self, sprite_sheet_path, frame_width, frame_height):
        self.sprite_sheet = Image.open(sprite_sheet_path)
        self.frame_width = frame_width
        self.frame_height = frame_height

    def remove_transparency(self, image, bg_color=(255, 255, 255)):
        if image.mode in ("RGBA", "LA") or (
            image.mode == "P" and "transparency" in image.info
        ):
            opaque_image = Image.new("RGB", image.size, bg_color)
            opaque_image.paste(
                image, mask=image.split()[3]
            )  # RGBA images have the alpha channel as the fourth band
            return opaque_image
        else:
            return image

    def get_frame(self, x, y):
        box = (
            x * self.frame_width,
            y * self.frame_height,
            (x + 1) * self.frame_width,
            (y + 1) * self.frame_height,
        )
        return self.sprite_sheet.crop(box)

    def extract_animation_frames(self, start_x, start_y, frame_count):
        frames = []
        current_x = start_x
        current_y = start_y
        for _ in range(frame_count):
            # frames.append(Image.new("RGBA", (128, 128), (0, 0, 0, 0)))
            opaque_frame = self.remove_transparency(
                self.get_frame(current_x, current_y), (0, 0, 0)
            )
            frames.append(opaque_frame)
            current_x += 1
            if current_x * self.frame_width >= self.sprite_sheet.width:
                current_x = 0
                current_y += 1
        return frames

    def create_animated_gif(self, frames, output_folder, duration=100, loop=0):
        frames[0].save(
            output_folder,
            save_all=True,
            append_images=frames[1:],
            duration=duration,
            loop=loop,
        )

    def create_animated_gif2(self, images, output_file, duration=100, loop=0):
        images[0].save(
            output_file,
            save_all=True,
            append_images=images[1:],
            optimize=False,
            duration=duration,
            loop=loop,
        )


def wrap(line, nl="\n\t"):
    """wraps a string within a terminal window"""
    nl = nl
    rows, columns = os.popen("stty size", "r").read().split()

    print(rows, columns)

    newline = ""
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
    print(
        wrap(
            "Usage: python gif_maker.py inpath=string_file outpath=string_folder name=string rows=int cols=int frame_width=int frame_height=int direction=(xy or yx) (xoffset=int) (yoffset=int) (image_type=str) (start_index=int 0,1) (isWang=True,False)"
        )
    )

    if command:
        if command == "extract":
            # Params in square brackets are optional
            # The kwargs function script needs the key value pairs (key=value) to NOT have spaces
            print(
                wrap(
                    "Example: python gif_maker.py infile=pacman_ghosts.png outfolder=pacman_ghosts_folder name=pacman_pink rows=9 cols=3 frame_width=40 frame_height=40 direction=xy xoffset=120 "
                )
            )
            print("")
        else:
            print(
                wrap(
                    "Example: python spriter.py infile=/path/to/images outfolder=/path/to/pacman_pink_ghost.png rows=9 cols=3 frame_width=40 frame_height=40 direction=xy"
                )
            )
            print("")

    sys.exit()


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

    print(argv)

    for arg in argv:
        if "=" in arg:
            key, val = arg.split("=")
            kargs[key] = val
        else:
            args.append(arg)
    return args, kargs


# Example usage
if __name__ == "__main__":
    """
    Sprite maker / extractor.
    """
    argv = sys.argv[1:]

    # process command line args
    args, kwargs = mykwargs(argv)

    infile = kwargs.get("infile", None)
    outfolder = kwargs.get("outfolder", None)
    name = kwargs.get("name", None)
    rows = kwargs.get("rows", None)
    cols = kwargs.get("cols", None)
    frame_width = kwargs.get("frame_width", None)
    frame_height = kwargs.get("frame_height", None)
    frame_count = kwargs.get("frame_count", None)
    direction = kwargs.get("direction", None)
    startx_frame = kwargs.get("startx_frame", 0)
    starty_frame = kwargs.get("starty_frame", 0)

    # sprite_sheet_path = "cowboy.png"
    # output_file = "shooting_right.gif"
    # frame_width = 128
    # frame_height = 128
    # startx_frame = 9
    # starty_frame = 0
    # frame_count = 4  # Set the number of frames in your animation
    
    if 'json' in infile:
        

    extractor = SpriteSheetExtractor(infile, frame_width, frame_height)
    frames = extractor.extract_animation_frames(startx_frame, starty_frame, frame_count)
    print(frames)
    i = 0
    for frame in frames:
        frame.save(f"{outfolder}/{name}_{i}.png")
        i += 1
    extractor.create_animated_gif2(frames, outfolder, duration=80, loop=1)

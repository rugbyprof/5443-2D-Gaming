from PIL import Image, ImageDraw, ImageFont


def get_font_size(text, font_name, pixel_size):
    """This returns the "font size" necessary to fit a letter in an image
       of a given pixel size. Different letters have different widths and
       heights.
    Params:
        text (str) : string to test
        font_name (str) : font to open
        pixel_size (int) : height of image
    Returns:
        font_size (int), font width (int) , font_height (int)

    """
    font_size = 12
    h = 0
    while h < pixel_size:
        font = ImageFont.truetype(font_name, font_size)
        w, h = font.getsize(text)
        font_size += 2
    return font_size, w, h


def makeTile(**kwargs):

    letter = kwargs.get("letter", "None")
    letter_color = kwargs.get("letter_color", "black")
    size = kwargs.get("size", (64, 64))
    fill_color = kwargs.get("fill_color", "white")
    border_size = kwargs.get("border_size", 3)
    border_color = kwargs.get("border_color", "black")
    border_radius = kwargs.get("border_radius", 7)
    font_ratio = kwargs.get("font_ratio", 0.9)
    underLine = kwargs.get("underLine", False)
    underLine_height = kwargs.get("underLine_height", 5)
    underLine_buffer = kwargs.get("underLine_buffer", (20, 20, 10))

    tile_width = size[0]
    tile_height = size[1]
    letter_size = int(tile_height * font_ratio)

    print(letter_size)

    font_size, font_width, font_hieght = get_font_size(letter, r"sans.ttf", letter_size)

    print(font_size, font_width, font_hieght)

    image = Image.new("RGBA", size)  # A 0-1
    # image = image.convert("RGBA")

    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle(
        (0, 0, tile_width, tile_height),
        fill=fill_color,
        outline=border_color,
        width=border_size,
        radius=border_radius,
    )

    font = ImageFont.truetype(r"sans.ttf", letter_size)

    # use the tile width and font width to center the letter. Same with the height.
    # the 1.30 is to shift the letter up a little bit. Not sure what will happen with a different font
    draw.text(
        (
            tile_width // 2 - (font_width // 2),
            tile_height // 2 - (font_hieght * 1.15 // 2),
        ),
        letter,
        font=font,
        fill=letter_color,
        align="middle",
    )

    if underLine:
        draw.rectangle(
            (
                (
                    underLine_buffer[0],
                    tile_height - underLine_buffer[2] - underLine_height,
                ),
                (tile_width - underLine_buffer[1], tile_height - underLine_buffer[2]),
            ),
            fill="white",
        )

    return image


if __name__ == "__main__":
    for letter in range(26):
        im = makeTile(
            letter=str(chr(letter + 65)),
            size=(512, 512),
            fill_color="black",
            border_size=3,
            border_color="red",
            border_radius=14,
            letter_color="white",
            underLine=True,
        )
        im.save(f"./letters/_{str(chr(letter+65))}.png")

    # val = 2
    # for i in range(11):
    #     im = makeTile(letter=str(val),size=(64,64),fill_color="black",border_size=2,border_color="red",border_radius=14,letter_color="white",font_ratio=.40)
    #     im.save(f"./letters/{str(val)}.png")

    #     val *= 2

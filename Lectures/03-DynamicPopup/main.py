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




def makePopUp(content,**kwargs):

    width = kwargs.get("width", 300)
    height = kwargs.get("height", 300)
    fill_color = kwargs.get("fill_color", "white")
    border_size = kwargs.get("border_size", 5)
    border_color = kwargs.get("border_color", "black")
    border_radius = kwargs.get("border_radius", 7)
    font_size = kwargs.get("font_size", 20)
    font_name = kwargs.get("font_name", "sans.ttf")
    # tile_width = size[0]
    # tile_height = size[1]



    # lineInfo = []
    # width = 0
    # height = 0
    # for key,line in content.items():
    #     font_size, font_width, font_height = get_font_size(line, r"sans.ttf", font_size)
    #     lineInfo.append({'font_size':font_size, 
    #     'font_width':font_width, 
    #     'font_height':font_height,
    #     'font':ImageFont.truetype(r"sans.ttf", font_size)})
    #     if font_width > width:
    #         width = font_width
    #     height += font_height
    
    #     print(font_size, font_width, font_height)
    
    # print(width,height)

    image = Image.new("RGBA", (width,height))  # A 0-1

    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle(
        (0, 0, width, height),
        fill=fill_color,
        outline=border_color,
        width=border_size,
        radius=border_radius,
    )

    

    # # use the tile width and font width to center the letter. Same with the height.
    # # the 1.30 is to shift the letter up a little bit. Not sure what will happen with a different font

    i = 0
    y = border_size
    totFontHeight = 0
    for line in content:
        if not 'font_size' in line:
            line['font_size'] = 20
        if not 'align' in line:
            align="center"
        
        if not line['align']:
            line['align'] = "left"



        if not 'font_name' in line:
            line['font_name'] = font_name

        print(line['font_name'])
            
        

        font_size, font_width, font_height = get_font_size(line['text'], line['font_name'], line['font_size'])

        font = ImageFont.truetype(line['font_name'], size=font_size)

        print(font_size, font_width, font_height)


        if not 'color' in line:
            color = "black"
        else:
            color = line['color']     
        
        x = border_size
        
        if line['align'] == 'center':
            x = ((width // 2) - (font_width // 2))
            #x = width // 2
        elif line['align'] == 'right':
            x = border_size + width - font_width
        draw.text((x,y),line['text'],font=font,fill=color,align='left')
        y += font_height + font_height // 2 + 5
        i += 1

    return image


if __name__ == "__main__":
    content = [
        {"text":"Window Title",'font_size':20,'align':'left','color':'white'},
        {"text":" ",'font_size':20,'align':'left','color':'white'},
        {"text":" Second Line ",'font_size':20,'align':'left','color':'white'},
        {"text":" Third Line centered Third Line centered ",'font_size':20,'align':'center','color':'white'},
        {"text":" Fourth Line Fourth Line Fourth Line ",'font_size':20,'align':'left','color':'white'},
        {"text":" Fifth Line ",'font_size':20,'align':'left','color':'white'},
        {"text":"This is a footer",'font_size':20,'align':'center','color':'white'}
    ]
    image = makePopUp(content,border_size=20,border_color='black',fill_color='green',width=600,height=275,font_name="Roboto-Bold.ttf")
    image.show()
    image.save(f"popup.png")

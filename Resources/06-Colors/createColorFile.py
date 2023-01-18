import json
from rich import print
import sys

colors = {
    "WHITE": "(255, 255, 255)",
    "BLACK": "(0, 0, 0)",
    "RED": "(230, 70, 70)",
    "BRIGHTRED": "(255, 0, 0)",
    "DARKRED": "(220, 0, 0)",
    "BLUE": "(0, 0, 255)",
    "SKYBLUE": "(135, 206, 250)",
    "PASTELBLUE": "(119, 158, 203)",
    "DARKBLUE": "(0, 35, 102)",
    "YELLOW": "(255, 250, 17)",
    "GREEN": "(110, 255, 100)",
    "ORANGE": "(255, 165, 0)",
    "DARKGREEN": "(60, 160, 60)",
    "DARKGREY": "(60, 60, 60)",
    "LIGHTGREY": "(180, 180, 180)",
    "BROWN": "(139, 69, 19)",
    "DARKBROWN": "(100, 30, 0)",
    "BROWNBLACK": "(50, 0, 0)",
    "GREYBROWN": "(160, 110, 90)",
    "CREAM": "(255, 255, 204)",
}


def loadExtraColors():
    with open("hex_color_names_rgb.json") as f:
        data = f.read()

        jdata = json.loads(data)

    exColors = {}
    for c in jdata:
        exColors[c["name"].upper()] = tuple(c["rgb"])

    return exColors


def saveExColors(exColors):

    for name, rgb in colors.items():
        if not name in exColors:
            exColors[name] = rgb
            print("new!!")

    colorList = []
    for name, rgb in exColors.items():
        t = tuple(rgb)
        colorList.append(f"{name} = {rgb}\n")

    colorList.sort()
    with open("temp.py", "w") as f:
        for c in colorList:
            f.write(f"{c}")


if __name__ == "__main__":
    exColors = loadExtraColors()
    saveExColors(exColors)

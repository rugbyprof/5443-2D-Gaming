import requests
from bs4 import BeautifulSoup
from rich import print
import html as htmlLib
import re
import json
from time import sleep

"""
Requirements: 
bs4
lxml
html5lib
requests
"""


def getPage(url, filename=None):
    r = requests.get(url)
    # print(res.status_code)
    if r.status_code == 200:
        if filename:
            with open(filename, "w") as f:
                f.write(htmlLib.unescape(r.text))
            return None
        tree = BeautifulSoup(r.text, features="html5lib")
        good = tree.prettify()
        return good
    return None


def getHtmlPage(fileName):

    with open(fileName) as f:
        data = f.read()

    return data


def hexToRgb(x):
    h = x.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


def getColors(html, outfile="colors.json"):
    colors = {}
    soup = BeautifulSoup(html, "lxml")

    divs = soup.find_all("tr", {"class": "tcw"})

    for div in divs:
        children = div.findChildren("td", recursive=False)
        name = None
        hex = None
        for child in children:
            if "#" in child.text.strip():
                hex = child.text.strip()
            else:
                name = child.text.strip().replace("(W3C)", "").strip()

        print(f"name: {name}")
        colors[name] = {}
        colors[name]["hex"] = hex
        colors[name]["rgb"] = hexToRgb(hex)
    print(len(colors))
    with open(outfile, "w") as f:
        json.dump(colors, f, indent=4, sort_keys=True)


if __name__ == "__main__":
    url = "https://www.computerhope.com/htmcolor.htm"
    html = getPage(url)
    getColors(html)

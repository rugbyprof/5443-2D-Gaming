import glob
import os

files = glob.glob("*.png")

for file in files:

    os.rename(file, file.lower())

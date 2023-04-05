"""
This is a helper file that wrote blanks and x's to a file to be read in as a set of platforms
"""

platforms = {
    20:[20,60],
    30:[10,40],
    40:[40,80],
    60:[5,60],
    79:[0,80]
}

f = open("map_temp.txt","w")

floor = False

for i in range(80):
    if i in platforms:
        cols = platforms[i]

        for t in range(cols[0]):
            f.write(' ')
        for t in range(cols[0],cols[1]):
            f.write('x')
        for t in range(cols[1],80):
            f.write(' ')
        f.write("\n")
    else:
        for t in range(80):
            f.write(' ')
        f.write("\n")

f.close()


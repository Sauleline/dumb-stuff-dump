from PIL import Image
import numpy
import os

print("...\"Folder Name\"\\\"Image Name\"")
image = input("where ")
os.system('cls')

with Image.open(image) as im:
    im = im.convert("L")

width, height = im.size

pixelValues = list(im.getdata())
pixelValues = numpy.array(pixelValues).reshape((width, height))

array = []
for x in range(width):
    array.append([])
    for y in range(height):
        array[x].append([])
        array[x][y] = "aaa"


array = numpy.array(array).reshape((width, height))
outString = ""

for i in range(width):
    for j in range(height):
        outString = str(pixelValues[i, j])
        array[i, j] = str(outString)

for i in range(width):
    for j in range(height):
        if 0 <= int(array[i, j]) <= 51:
            array[i, j] = "  "
        elif 52 <= int(array[i, j]) <= 102:
            array[i, j] = "░░"
        elif 103 <= int(array[i, j]) <= 154:
            array[i, j] = "▒▒"
        elif 155 <= int(array[i, j]) <= 205:
            array[i, j] = "▓▓"
        elif 206 <= int(array[i, j]) <= 254:
            array[i, j] = "██"
        else:
            array[i, j] = "  "
#numpy.set_printoptions(threshold= numpy.inf)
#print(array)
display = ""

shapeH, shapeW = numpy.shape(array)

for x in range(shapeH):
    display = ""
    for y in range(shapeW):
        display += str(array[x, y])
    print(display)

input()

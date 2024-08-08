from PIL import Image
import numpy
import os

def mapRange(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

image = input("file name: ")
os.system('cls')

with Image.open(image) as im:
    im = im.resize((64, 64))
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

texture = ["  ", "░░", "▒▒", "▓▓", "██"]

array = numpy.array(array).reshape((width, height))
outString = ""

for i in range(width):
    for j in range(height):
        outString = str(pixelValues[i, j])
        array[i, j] = str(outString)

for i in range(width):
    for j in range(height):
        array[i, j] = texture[mapRange(int(array[i, j]), 0, 255, 0, len(texture)-1)]

display = ""

shapeH, shapeW = numpy.shape(array)

for x in range(shapeH):
    display = ""
    for y in range(shapeW):
        display += str(array[x, y])
    print(display)

input()

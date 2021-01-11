from PIL import Image
import random

def pixelDiv(i, j, imageObject : Image.Image, firstValue, test):
    values = None
    if firstValue == 255:
        values = [255, 0]
    elif firstValue == 0:
        values = [0, 255]
    else:
        raise ValueError(firstValue)
    if not test:
        imageObject.putpixel((i*2, j), values[0])
        imageObject.putpixel((i*2+1, j), values[1])
    else:
        imageObject.putpixel((i*2, j*2), values[0])
        imageObject.putpixel((i*2+1, j*2), values[1])
        imageObject.putpixel((i*2, j*2+1), values[0])
        imageObject.putpixel((i*2+1, j*2+1), values[1])

def encrypt(imagePath, outputPath1, outputPath2, test):
    image = Image.open(imagePath)
    image = image.convert('1')
    out1 = None
    out2 = None
    if test:
        out1 = Image.new('1', [size*2 for size in image.size])
        out2 = Image.new('1', [size*2 for size in image.size])
    else:
        out1 = Image.new('1', [image.size[0]*2, image.size[1]])
        out2 = Image.new('1', [image.size[0]*2, image.size[1]])

    for i in range(0, image.size[0], 1):
        for j in range(0, image.size[1], 1):
            pixel = image.getpixel((i,j))
            
            x = random.randint(0,1)
            if pixel == 0: #black
                if x == 0:
                    pixelDiv(i,j,out1,255, test)
                    pixelDiv(i,j,out2,0, test)
                else:
                    pixelDiv(i,j,out1,0, test)
                    pixelDiv(i,j,out2,255, test)
            if pixel == 255: #white
                if x == 0:
                    pixelDiv(i,j,out1,255, test)
                    pixelDiv(i,j,out2,255, test)
                else:
                    pixelDiv(i,j,out2,0, test)
                    pixelDiv(i,j,out1,0, test)
    out1.save(outputPath1)
    out2.save(outputPath2)

def dectypt(imagePath1, imagePath2, outputPath):
    inImage1 = Image.open(imagePath1)
    inImage2 = Image.open(imagePath2)
    image = Image.new('1', [size for size in inImage1.size])
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            image.putpixel((x, y), min(inImage1.getpixel((x, y)), inImage2.getpixel((x, y))))
    image.save(outputPath)
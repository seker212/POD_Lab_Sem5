import numpy
from os import SEEK_END

def writeToBitmap(bitmapFilePath, textFilePath, outputBitmapFilePath):
    BitsArrayPic = numpy.unpackbits(numpy.fromfile(bitmapFilePath, dtype = "uint8"))
    BitsArrayText = numpy.unpackbits(numpy.fromfile(textFilePath, dtype = "uint8"))
    i = 54 
    for b in BitsArrayText: 
        BitsArrayPic[i*8+7] = b 
        i = i+1 
    for x in range(16): 
        BitsArrayPic[i*8+7] = 1
        i = i+1
    with open(outputBitmapFilePath,"wb") as outputfile:
        outputfile.write(numpy.packbits(BitsArrayPic)) 

def readFromBitmap(bitmapFilePath, outputTextFilePath):
    picBits = numpy.unpackbits(numpy.fromfile(bitmapFilePath, dtype = "uint8")) 
    i = 54 
    with open(outputTextFilePath,"wb") as outputfile: 
        checkEnd = []
        outputBits = []
        while True:
            for x in range(8): 
                outputBits.append(picBits[i*8+7])
                i = i+1
            if((outputBits == checkEnd == [1,1,1,1,1,1,1,1]) or i >= len(picBits)/8):
                outputfile.seek(-1, SEEK_END)
                outputfile.truncate()
                break
            else: 
                checkEnd = outputBits.copy() 
                outputfile.write(numpy.packbits(outputBits)) 
                outputBits = [] 


# TEST MAIN
# writeToBitmap('in.bmp', 'tekst.txt', 'out.bmp')
# readFromBitmap('out.bmp', 'out.txt')
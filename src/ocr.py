from tesserocr import PyTessBaseAPI
from PIL import Image, ImageChops
import os

path_img = "./img"


def isThisBlack(image):
    black = False
    treshold = 10
    imlist = list(image.getdata())
    colorsum = 0
    for pixel in imlist:
        colorsum += pixel
    return(colorsum/len(imlist) < treshold)


def samePicture(image1, image2):
    return(isThisBlack(ImageChops.difference(image1, image2)))


def getLetterDict(path):
    """
    Input : The directory where identified letters are stored\n
    Output : A dictionnary : keys are letters, elements are pictures

    """
    result = {}
    for letter in os.listdir(f"{path}"):

        imletter = Image.open(f"{path}/{letter}")
        result[letter] = imletter
    return(result)


def getListOfSquares(path):
    """
    Gets letters by hand
    @param: The path to a Word Blitz screenshot
    @returns : A list of 16 square images containing the letters of the image
    """

    # Let's get the picture of this screenshot (L is for grey leveling)
    fullimage = Image.open(path).convert("L")

    squares = []
    squares.append(fullimage.crop((66, 643, 283, 859)))  # row one
    squares.append(fullimage.crop((310, 643, 527, 859)))  # row one
    squares.append(fullimage.crop((554, 643, 771, 859)))  # row one
    squares.append(fullimage.crop((798, 643, 1015, 859)))  # row one

    squares.append(fullimage.crop((66, 887, 283, 1103)))  # row two
    squares.append(fullimage.crop((310, 887, 527, 1103)))  # row two
    squares.append(fullimage.crop((554, 887, 771, 1103)))  # row two
    squares.append(fullimage.crop((798, 887, 1015, 1103)))  # row two

    squares.append(fullimage.crop((66, 1131, 283, 1347)))  # row three
    squares.append(fullimage.crop((310, 1131, 527, 1347)))  # row three
    squares.append(fullimage.crop((554, 1131, 771, 1347)))  # row three
    squares.append(fullimage.crop((798, 1131, 1015, 1347)))  # row three

    squares.append(fullimage.crop((66, 1375, 283, 1591)))  # row four
    squares.append(fullimage.crop((310, 1375, 527, 1591)))  # row four
    squares.append(fullimage.crop((554, 1375, 771, 1591)))  # row four
    squares.append(fullimage.crop((798, 1375, 1015, 1591)))  # row four

    # More cropping : we only want to get the letter
    inc = 70  # The number of pixels by witch we crop our squares
    for i in range(len(squares)):
        squares[i] = squares[i].crop((inc, inc, 216 - inc, 216 - inc))
    return(squares)


def getGrid(imgpath, letterpath):
    """
    Input : path to a Word Blitz screenshot\n
    Output : a grid corresponding to the letters in this screenshot
    """

    grid = []
    squares = getListOfSquares(imgpath)
    letters = getLetterDict(letterpath)

    # Goes through each square in order and compares it to identified letters
    for square in squares:
        for letter in letters.keys():
            if (samePicture(square, letters[letter])):
                grid.append(letter)

    return(grid)

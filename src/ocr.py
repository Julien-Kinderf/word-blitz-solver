from tesserocr import PyTessBaseAPI
from PIL import Image, ImageChops
import os

path_img = "./img"


def isThisBlack(image):
    black = False
    treshold = 15
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

    # These are squares of 220*220 pixels, spaced from each other by 27 pixels
    # The top left corner is at 60, 659
    square_dim = 220
    square_space = 27
    increment = 70

    start_tlx = 60
    start_tly = 659
    squares = []
    for row in range(4):
        for col in range(4):
            tlx = start_tlx + col * (square_dim + square_space)
            tly = start_tly + row * (square_dim + square_space)
            brx = tlx + square_dim
            bry = tly + square_dim
            square = fullimage.crop((tlx, tly, brx, bry))
            # just cropping a little more
            square = square.crop((increment, increment,
                                  square_dim - increment, square_dim - increment))
            squares.append(square)

    if (len(squares) != 16):
        print(
            f"Unable to detect 16 squares. You are probably missing a letter in identified.")
        exit(1)
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

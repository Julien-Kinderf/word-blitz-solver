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


def getListOfSquares(fullimage, idfull):
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

    # More cropping
    inc = 70
    for i in range(len(squares)):
        squares[i] = squares[i].crop((inc, inc, 216 - inc, 216 - inc))
        squares[i].save(f"./img/cropped/image{idfull}-{i}.png")

    return(squares)


def getAllSquares():
    id = 0
    for file in os.listdir(path_img + "/full/"):
        print(path_img + "/full/" + file)
        image = Image.open(path_img + "/full/" + file).convert("L")
        getListOfSquares(image, id)
        id += 1


def identify():
    # Asks the user to identify letters in the cropped section
    # Once identified, the file is renamed to LETTER.png
    found = []
    # For all non analysed cropped letter
    for letter in os.listdir(path_img + "/cropped/"):
        if (letter == ".directory"):  # This one is not an image
            continue

        imletter = Image.open(f"{path_img}/cropped/{letter}")  # Get the image
        imletter.show()
        name = input("Quelle lettre vient de s'afficher ? ")

        found.append(name)
        os.rename(f"{path_img}/cropped/{letter}",
                  f"{path_img}/identified/{name}")


def loadletters():
    result = {}
    for letter in os.listdir(f"{path_img}/identified"):

        imletter = Image.open(f"{path_img}/identified/{letter}")
        result[letter] = imletter
    return(result)


def getGrid(imgpath):
    fullimage = Image.open(imgpath).convert("L")

    grid = []
    squares = getListOfSquares(fullimage, 1)
    letters = loadletters()

    column = 0
    for square in squares:
        for letter in letters.keys():
            if (samePicture(square, letters[letter])):
                grid.append(letter)

    return(grid)

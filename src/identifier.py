"""
this script is used to identify the letters contained
in the img/full folder.
"""
import os
from PIL import Image, ImageChops

# Global
dirname = os.path.dirname(__file__)
projectroot = dirname.replace("/src", '')


def isThisBlack(image):
    """
    Determines if the picture is almost black
    @param : PIL image
    @returns : True if the image is almost black, False if not
    """
    black = False
    treshold = 10
    imlist = list(image.getdata())
    colorsum = 0
    for pixel in imlist:
        colorsum += pixel
    return(colorsum/len(imlist) < treshold)


def samePicture(image1, image2):
    """
    Returnds True if both images are almost the same
    """
    return(isThisBlack(ImageChops.difference(image1, image2)))


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


def identify(path):
    """
    Loads the letters of the screenshots in img/toidentify
    Shows them one by one
    Asks the user to enter the corresponding letter
    Saves them in img/identified
    @param : the relative path to the images to identify folder
    """

    for screenshot in os.listdir(projectroot + path):
        # My file manager sometimes adds .directory files
        if (screenshot == ".directory"):
            continue

        screenshot_squares = getListOfSquares(
            projectroot + path + '/' + screenshot)

        for square in screenshot_squares:
            squareisknown = False
            # Let's see if we don't already have this picture in img/identified
            for known_square in os.listdir((projectroot + "/img/identified")):
                temp = Image.open(
                    projectroot + "/img/identified/" + known_square).convert("L")

                if (samePicture(temp, square)):
                    squareisknown = True
                    break

            if not squareisknown:
                # I've never seen this square in my life
                square.show()
                squareletter = input("What letter is that ?")
                square.save(f"{projectroot}/img/identified/{squareletter}.png")
                os.rename(f"{projectroot}/img/identified/{squareletter}.png",
                          f"{projectroot}/img/identified/{squareletter}")
                print(
                    f"Letter {squareletter} identified and saved to /img/identified")


if __name__ == "__main__":

    path = "/img/toidentify"
    identify(path)

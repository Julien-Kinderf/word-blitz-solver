"""
this script is used to identify the letters contained
in the img/full folder.
"""
import os
import sys
from PIL import Image, ImageChops
import ocr

# Global
dirname = os.path.dirname(__file__)
projectroot = dirname.replace("/src", '')


def identify(path):
    """
    Loads the letters of the screenshots in img/toidentify
    Shows them one by one
    Asks the user to enter the corresponding letter
    Saves them in img/identified
    @param : the relative path to the images to identify folder
    """
    identifiedpath = path.replace("toidentify", "identified")

    for screenshot in os.listdir(projectroot + path):
        # My file manager sometimes adds .directory files
        if (screenshot == ".directory"):
            continue

        screenshot_squares = ocr.getListOfSquares(
            projectroot + path + '/' + screenshot)

        for square in screenshot_squares:
            squareisknown = False
            # Let's see if we don't already have this picture in img/identified
            for known_square in os.listdir((projectroot + identifiedpath)):
                temp = Image.open(
                    projectroot + identifiedpath + known_square).convert("L")

                if (ocr.samePicture(temp, square)):
                    squareisknown = True
                    break

            if not squareisknown:
                # I've never seen this square in my life
                square.show()
                squareletter = input("What letter is that ?")
                name = f"{squareletter}.png"
                if (squareletter not in os.listdir(f"{projectroot}{identifiedpath}")):
                    square.save(
                        f"{projectroot}{identifiedpath}{squareletter}.png")
                    os.rename(f"{projectroot}{identifiedpath}{squareletter}.png",
                              f"{projectroot}{identifiedpath}{squareletter}")
                else:
                    n = len([f for f in os.listdir(
                        f"{projectroot}{identifiedpath}") if f[0] == squareletter])
                    print(f"This letter had already been registered {n} times")
                    square.save(
                        f"{projectroot}{identifiedpath}{squareletter}.png")
                    os.rename(f"{projectroot}{identifiedpath}{squareletter}.png",
                              f"{projectroot}{identifiedpath}{squareletter}{n+1}")
                print(
                    f"Letter {squareletter} identified and saved to /img/identified")


if __name__ == "__main__":

    path = os.path.abspath(__file__).replace(
        "/src/identifier.py", "/img/toidentify/")

    identify(path)

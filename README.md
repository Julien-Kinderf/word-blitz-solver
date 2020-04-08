# word-blitz-solver

This small project a solver for the facebook game "word blitz"

Steps taken :
- Get a bunch of screenshots of the game and pu them in *img/full*
- use the identify script to display each cropped letter of these screens and ask the user for an identification of the letter, since the tesseract ocr functions didn't work. The identified cropped letters are stored in *img/identified* and are used by the solver script to determine the grid of the wanted game.
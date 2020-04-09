#!/usr/bin/python3
"""
This script
"""

import sys
import os
import time
import ocr


def neighboors(case):
    """
    Returns the list of neighboors of the input node, following our grid convention
    """

    # Switch case made with a dictionnary
    n = {0: [1, 4, 5],
         1: [0, 2, 5, 6, 4],
         2: [1, 3, 6, 7, 5],
         3: [2, 7, 6],

         4: [0, 1, 5, 9, 8],
         5: [4, 6, 1, 9, 0, 10, 2, 8],
         6: [5, 7, 2, 10, 1, 11, 3, 9],
         7: [2, 3, 6, 10, 11],

         8: [4, 5, 9, 12, 13],
         9: [8, 10, 5, 13, 4, 14, 6, 12],
         10: [9, 11, 6, 14, 5, 15, 7, 13],
         11: [6, 7, 10, 14, 15],

         12: [13, 8, 9],
         13: [12, 14, 9, 8, 10],
         14: [13, 15, 10, 9, 11],
         15: [14, 11, 10, ]}
    return(n[case])


def getstring(chemin, grille):
    """Renvoie la chaine de caractères correspondant au chemin fourni en entrée"""
    s = "".join([grille[i] for i in chemin])
    return(s)


def cleandict(path, grid):
    """Nettoie le dictionnaire en retirant tous les mots non faisables"""
    with open(path, "r+") as textfile:
        text = textfile.read().split()

    dictionnaire = []
    startsize = len(text)

    for mot in text:
        if not ((len(mot) == 1) or (len(mot) >= 17) or ("-" in mot) or not (set(mot) <= set(grid))):
            dictionnaire.append(mot)

    endsize = len(dictionnaire)
    return(dictionnaire)


def solve(grid, path_to_dict):
    """
    @parameter : a grid of letters
    @output : a dictionnary : keys are possible words and elements are the necessary moves
    """
    motstrouves = {}

    # Récupération du dictionnaire
    dictionnaire = cleandict(path_to_dict, grid)
    # Initialisation des chemins de base :
    # (ce sont juste des numéros de cases)
    chemins = []
    for i in range(16):
        chemins.append([i])

    # On évalue tour à tour chaque chemin
    while len(chemins) > 0:
        chemin = chemins[0]
        # print(f"Etude du chemin {chemin}")
        # Pour chacun de ces chemins on regarde l'ensemble des voisins de sa dernière case
        # Naturellement, on en exclut les voisins qui sont déjà dans le chemin
        voisins = [v for v in neighboors(chemin[-1]) if v not in chemin]

        # On observe à présent chacun de ces voisins :
        for voisin in voisins:
            found = False
            # print(f"\tEtude du voisin {voisin} :")
            # On regarde le nouveau chemin potentiel et la chaine associée
            newchemin = chemin[:]
            newchemin.append(voisin)
            # ex: [0, 1] devient [0, 1, 2]

            newchaine = getstring(newchemin, grid)
            # print(f"\t\tchemin {newchemin} pour chaine {newchaine} : ", end="")
            # On compare à ce qu'on a dans le dictionnaire :
            # Si il y a un match c'est chouette
            if ((newchaine not in motstrouves.keys()) and (newchaine in dictionnaire)):
                chemins.append(newchemin)
                found = True
                motstrouves[newchaine] = newchemin
                # print("trouvé dans le dictionnaire")
                continue  # Puisque la chaine est un mot il y a des bonnes chances qu'il existe aussi d'autres chaines qui commencent par ce mot

            # On peut quand même espérer un match si des mots commencent par cette chaine
            for mot in dictionnaire:
                if (mot.startswith(newchaine)):
                    chemins.append(newchemin)
                    found = True
                    # print(f"Début de la chaine {mot}")
                    break  # Il suffit de trouver un mot qui commence par cette chaine pour que ça vaille le coup de la garder

            if not found:
                # print("pas dans le dictionnaire")
                pass
                # Après l'avoir analysé on supprime le chemin

        chemins.remove(chemin)
    return(motstrouves)


"""
solution = solve(grid)

for mot in solution.keys():
    print(f"{mot} : {solution[mot]}")
print(f"Temps d'execution : {time.time() - start_time} secondes")
"""
if __name__ == "__main__":
    start_time = time.time()
    os.system('clear')
    if (len(sys.argv) != 2):
        print(f"Usage : python3 solver.py <path to your image>")
        exit(0)

    # Retrieving the input file
    relative_path_to_image = sys.argv[1]
    if (os.path.exists(relative_path_to_image)):
        absolute_path_to_image = os.path.abspath(relative_path_to_image)
    else:
        print(f"Cannot find {relative_path_to_image}")
        exit(1)

    # Retrieving the identified letter folder path
    absolute_path_to_letters = __file__.replace(
        "/src/solver.py", "/img/identified/")

    # Retrieving the identified letter folder path
    absolute_path_to_exec = __file__.replace(
        "/solver.py", "/executioner.sh")

    # Retrieving the path for the used dictionnary
    absolute_path_to_dictionnary = __file__.replace(
        "/src/solver.py", "/words/dictionnary.txt")
    # getting the grid
    grid = ocr.getGrid(absolute_path_to_image, absolute_path_to_letters)
    print(
        f"Detected the following grid in {round(time.time() - start_time, 2)} seconds :\n{' '.join(grid[0:4])}\n{' '.join(grid[4:8])}\n{' '.join(grid[8:12])}\n{' '.join(grid[12:16])}\n")

    # Beginning of the word research phase
    print("Starting the word research ...")
    research_start_time = time.time()
    solution = solve(grid, absolute_path_to_dictionnary)
    research_end_time = time.time()

    print(
        f"Found {len(solution)} possible words in {round(research_end_time - research_start_time, 2)} seconds :")
    for word in solution.keys():
        print(f"{word} ({len(word)}): {solution[word]}")

    print(
        f"Found {len(solution)} words in {round(time.time() - start_time, 2)} seconds")

    # exit()  # What follows is not ready yet
    print()
    typing_start = time.time()
    print(f"Starting to send words to the phone :")
    nbwords = 0
    for word in sorted(solution.keys(), reverse=True, key=lambda w: len(w)):
        print(f"Entering word {word}")
        pattern = ' '.join([str(i) for i in solution[word]])
        os.system(f"bash {absolute_path_to_exec} {pattern}")
        nbwords += 1

        if ((time.time() - start_time) > 40):  # Put this value to 78 to play all time
            break

    print(
        f"Entered {nbwords} words in {round(time.time() - typing_start, 2)} seconds")

import time
import ocr
start_time = time.time()

pathdict = "words/liste.txt"
pathimg = "img/tosolve.jpg"

grid = ocr.getGrid(pathimg)
print(grid)


def neighboors(case):

    # Renvoie la liste des voisins de la case donnée en entrée
    # Fonctionne uniquement pour ce problème précis puisqu'on imagine une grille carrée de côté 4
    voisins = {0: [1, 4, 5],
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
    return(voisins[case])


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
        if not ((len(mot) == 1) or (len(mot) >= 16) or ("-" in mot) or not (set(mot) <= set(grid))):
            dictionnaire.append(mot)

    endsize = len(dictionnaire)
    print(
        f"Dictionnaire passé de {startsize} à {endsize} mots ({endsize - startsize})")
    return(dictionnaire)


def solve(grid):
    """
    @parameter : a grid of letters
    @output : a dictionnary : keys are possible words and elements are the necessary moves
    """

    motstrouves = {}

    # Récupération du dictionnaire
    dictionnaire = cleandict(pathdict, grid)
    # Initialisation des chemins de base :
    # (ce sont juste des numéros de cases)
    chemins = []
    for i in range(16):
        chemins.append([i])

    # On évalue tour à tour chaque chemin
    for chemin in chemins:
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


solution = solve(grid)

for mot in solution.keys():
    print(f"{mot} : {solution[mot]}")
print(f"Temps d'execution : {time.time() - start_time} secondes")

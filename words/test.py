path = "/home/julien/Documents/Projets/word-blitz-solver/words/dictionnary.txt"
with open(path, "r+") as textfile:
        text = textfile.read().split()

    dictionnaire = []
    startsize = len(text)

    for mot in text:
        if not ((len(mot) == 1) or (len(mot) >= 17) or ("-" in mot) or not (set(mot) <= set(grid))):
            dictionnaire.append(mot)

    endsize = len(dictionnaire)
    return(dictionnaire)

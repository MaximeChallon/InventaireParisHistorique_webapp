# Script non utilisé dans l'application
import csv
from collections import Counter

with open('/home/maxime/dev/InventaireParisHistorique_files/exports/Inventaire_general_phototheque.csv', 'r') as f:
    f_o = csv.reader(f, delimiter='|')
    next(f_o)
    next(f_o)
    liste_mots_cles = []
    for row in f_o:
        if row[33] is not None and row[33] != '':
            if row[27] is not None and row[27] != '':
                liste_mots_cles.append(row[27])
            if row[26] is not None and row[26] != '':
                liste_mots_cles.append(row[26])
            if row[25] is not None and row[25] != '':
                liste_mots_cles.append(row[25])
            if row[24] is not None and row[24] != '':
                liste_mots_cles.append(row[24])
            if row[23] is not None and row[23] != '':
                liste_mots_cles.append(row[23])
            if row[22] is not None and row[22] != '':
                liste_mots_cles.append(row[22])
    sortie = Counter(liste_mots_cles).most_common()
    markdown = ""
    for mot in sortie:
        markdown= markdown + "* " + mot[0] + " (" + str(mot[1]) + ")\n"
    print(markdown)
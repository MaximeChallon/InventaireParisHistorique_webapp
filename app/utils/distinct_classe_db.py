from ..app import db
from collections import Counter


ARRONDISSEMENTS = [ (art[0], art[0]) for art in db.session.execute("""select distinct Arrondissement from Classe_db where Arrondissement != '' order by Arrondissement""")]

liste_mots_cles = []
for row in db.session.execute("""select Mot_cle1 , Mot_cle2 , Mot_cle3 , Mot_cle4 , Mot_cle5, Mot_cle6 
from Classe_db  
"""):
    if row is not None and row != '':
        if row[0] is not None and row[0] != '':
            liste_mots_cles.append(row[0])
        if row[1] is not None and row[1] != '':
            liste_mots_cles.append(row[1])
        if row[2] is not None and row[2] != '':
            liste_mots_cles.append(row[2])
        if row[3] is not None and row[3] != '':
            liste_mots_cles.append(row[3])
        if row[4] is not None and row[4] != '':
            liste_mots_cles.append(row[4])
        if row[5] is not None and row[5] != '':
            liste_mots_cles.append(row[5])
MOTS_CLES = [(mc[0], mc[0] + " (" + str(mc[1]) + ")")for mc in Counter(liste_mots_cles).most_common()]

SUPPORTS = [ (art[0], art[0]) for art in db.session.execute("""select distinct Support from Classe_db where Support != '' order by Support""")]

TAILLES = [ (art[0], art[0]) for art in db.session.execute("""select distinct Taille from Classe_db where Taille != '' order by Taille""")]

PHOTOGRAPHES = [ (art[0], art[0]) for art in db.session.execute("""select distinct Photographe from Classe_db where Photographe != '' order by Photographe""")]

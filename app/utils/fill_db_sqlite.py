import csv
import re

# AVERTISSEMENT: ce script n'est pas utilisé dans l'application
# il permet simplement de remplir la bse de données db.sqlite quand de nouvelles données ont été catalogué

def quote(col):
    if col is None:
        return ''
    # uses double-quoting style to escape existing quotes
    return '"{}"'.format(re.sub("\n","",str(col).replace('"', '""')))

with open('/home/maxime/dev/InventaireParisHistorique_files/exports/Inventaire_general_phototheque.csv', 'r') as f:
	with open('/home/maxime/dev/InventaireParisHistorique_files/exports/pour_db/inventaire_complet.csv', "w") as f_e:
		f_o = csv.reader(f, delimiter='|')
		next(f_o)
		liste_labels = ["N_inventaire", "Rue", "N_rue", "Nom_site", "Arrondissement", "Ville", "Département", "Latitude_x",
						"Longitude_y", "Support", "Couleur", "Taille", "Date_prise_vue", "Photographe", "Droits",
						"Mention_don", "Mention_collection", "Date_construction", "Architecte", "Classement_MH", "Légende",
						"Generalite_architecture", "Mot_cle1", "Mot_cle2", "Mot_cle3", "Mot_cle4", "Mot_cle5", "Mot_cle6",
						"Autre_adresse", "Notes", "Cote_base", "Cote_classement", "Date_inventaire", "Auteur"]

		liste_champs_utiles = [0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 17, 18, 19, 21, 22, 23, 24, 25, 26, 27, 30, 31, 32, 33]
		ligne_finale = []
		for champ in liste_champs_utiles:
			ligne_finale.append(quote(liste_labels[champ]))
		f_e.write(';'.join(ligne_finale) + '\n')
		for row in f_o:
			if row[33] != '' and "LIOT" not in row[13] and "LIOT" not in row[14] and "LIOT" not in row[15]:
				ligne_finale = []
				for champ in liste_champs_utiles:
					ligne_finale.append(quote(row[champ]))
				f_e.write(';'.join(ligne_finale) + '\n')
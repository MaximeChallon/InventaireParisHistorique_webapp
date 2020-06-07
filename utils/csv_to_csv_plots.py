import csv

with open('/home/maxime/Documents/PH/Inventaire/inventaire_complet.csv', 'r') as f:
	with open('../app/statics/data/inventaire_complet.csv', "w") as f_e:
		f_csv = csv.writer(f_e)
		f_o = csv.reader(f, delimiter='¤', quotechar='£')
		next(f_o)
		next(f_o)
		liste_labels = ["N_inventaire", "Rue", "N_rue", "Nom_site", "Arrondissement", "Ville", "Département", "Latitude_x",
						"Longitude_y", "Support", "Couleur", "Taille", "Date_prise_vue", "Photographe", "Droits",
						"Mention_don", "Mention_collection", "Date_construction", "Architecte", "Classement_MH", "Légende",
						"Généralité_architecture", "Mot_cle1", "Mot_cle2", "Mot_cle3", "Mot_cle4", "Mot_cle5", "Mot_cle6",
						"Autre_adresse", "Notes", "Cote_base", "Cote_classement", "Date_inventaire", "Auteur"]

		liste_champs_utiles = [0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 17, 18, 19, 21, 22, 23, 24, 25, 26, 27, 30, 31, 32]
		f_csv.writerow(["N_inventaire", "Rue", "N_rue", "Nom_site", "Arrondissement", "Ville", "Latitude_x", "Longitude_y", "Support", "Couleur", "Taille", "Date_prise_vue", "Photographe", "Date_construction", "Architecte", "Classement_MH", "Généralité_architecture", "Mot_cle1", "Mot_cle2", "Mot_cle3", "Mot_cle4", "Mot_cle5", "Mot_cle6", "Cote_base", "Cote_classement", "Date_inventaire"])
		for row in f_o:
			if row[7] != '' and "PONTY" not in row[13] and "PONTY" not in row[14] and "PONTY" not in row[15]:
				ligne_finale = []
				for champ in liste_champs_utiles:
					ligne_finale.append(row[champ])
				f_csv.writerow(ligne_finale)
import json
import csv
import datetime

today = str(datetime.date.today())

with open('/home/maxime/Documents/PH/Inventaire/inventaire_complet.csv', 'r') as f:
	f_o = csv.reader(f, delimiter='¤', quotechar='£')
	i = 0
	next(f_o)
	next(f_o)
	liste_labels = ["N_inventaire", "Rue", "N_rue", "Nom_site", "Arrondissement", "Ville", "Département", "Latitude_x",
					"Longitude_y", "Support", "Couleur", "Taille", "Date_prise_vue", "Photographe", "Droits",
					"Mention_don", "Mention_collection", "Date_construction", "Architecte", "Classement_MH", "Légende",
					"Généralité_architecture", "Mot_cle1", "Mot_cle2", "Mot_cle3", "Mot_cle4", "Mot_cle5", "Mot_cle6",
					"Autre_adresse", "Notes", "Cote_base", "Cote_classement", "Date_inventaire", "Auteur"]

	json_final = {"data": {}, "date_creation": today, "auteur": "automatique via script Python3"}
	j = 0
	liste_champs_utiles = [0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 22, 23, 24, 25, 26, 27, 30, 31]
	for row in f_o:
		dico_item = {}
		if row[7] != '' and "PONTY" not in row[13] and "PONTY" not in row[14] and "PONTY" not in row[15]:
			for champ in liste_champs_utiles:
				dico_item[liste_labels[champ]] = row[champ]
			json_final['data'][j] = dico_item
			j += 1
		i += 1
	with open('../app/statics/data/inventaire_complet.json', "w") as f_e:
		f_e.write(json.dumps(json_final))

# json final {
	#data:[
	#{"rue": "blabla"},
	#]
#}
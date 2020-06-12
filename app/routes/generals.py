from flask import render_template, jsonify
from ..app import app
from ..models.graphiques import classe_graphiques
import pandas as pd
import csv
from ..models.donnees import Classe_db


@app.route("/")
def accueil():
	return render_template("pages/accueil.html")


#les routes cratographie et json_carto vont ensemble: la première affiche le html, la seconde fournit à Ajax de la première le JSON nécessaire
@app.route("/cartographie")
def cartographie():
	return render_template("pages/cartographie.html")


@app.route("/json_carto")
def json_carto():
	data = {}
	i = 0
	for photo in Classe_db.query.all():
		data[str(i)] = photo.to_json()
		i += 1
	json_array = {"data": data}
	return json_array


# les routes suivantes vont ensemble: la première gère l'affichage des graphiques, les autres contiennent seulement le JSOn nécessaire aux graphiques
@app.route("/graphiques")
def graphiques():
	return render_template("pages/graphiques.html")


@app.route("/graphiques/temporels")
def temporels():
	liste = [[x.Date_inventaire] for x in Classe_db.query.all()]

	#données au jour le jour
	data_jour = pd.DataFrame(liste, columns=["Date_inventaire"])
	data_jour["Date_inventaire"] = pd.to_datetime(data_jour["Date_inventaire"], format="%Y/%m/%d")
	data_jour["occurences"] = 1
	general_au_jour = data_jour.groupby("Date_inventaire", as_index=False).sum()

	#données par mois
	dico_mois = {}
	for photo in liste:
		if photo[0][0:7] not in dico_mois and photo[0] != "":
			dico_mois[photo[0][0:7]] = 1
		elif photo[0][0:7] in dico_mois and photo[0] != "":
			dico_mois[photo[0][0:7]] = dico_mois[photo[0][0:7]] + 1
	liste_mois = []
	dico_annee = {"01": 31, "02": 29, "03": 31, "04": 30, "05": 31, "06":30, "07": 31, "08": 31, "09": 30, "10": 31, "11": 30, "12": 31}
	for cle in dico_mois:
		if cle[5:7] in dico_annee:
			for jour in range(1, dico_annee[cle[5:7]]):
				liste_mois.append([cle + "/"+ str(jour), dico_mois[cle]])
	data_mois = pd.DataFrame(liste_mois)
	data_mois.columns = ["Date_inventaire", 'occurences']
	data_mois['Date_inventaire'] = pd.to_datetime(data_mois['Date_inventaire'], format="%Y/%m")

	chart = classe_graphiques.generate_temporels_bar(data_mois, "Mois et jour")
	return chart.to_json()
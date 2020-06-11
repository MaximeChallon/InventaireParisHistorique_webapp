from flask import render_template
from ..app import app
from ..models.graphiques import classe_graphiques
import pandas as pd
import csv
from ..constantes import *


@app.route("/")
def accueil():
    return render_template("pages/accueil.html")


@app.route("/cartographie")
def cartographie():
	return render_template("pages/cartographie.html")


@app.route("/graphiques")
def graphiques():
	return render_template("pages/graphiques.html")


@app.route("/graphiques/temporels")
def temporels():
	#pour les graphiques au jour le jour
	data_jour = pd.read_csv(CSV_GRAPHIQUES)
	data_jour["Date_inventaire"] = pd.to_datetime(data_jour["Date_inventaire"], format="%Y/%m/%d")
	#ajout colonne occurences
	data_jour["occurences"] = 1
	general_au_jour = data_jour.groupby("Date_inventaire", as_index=False).sum()

	#pour les graphiques par mois
	with open(CSV_GRAPHIQUES) as f:
		f_o = csv.reader(f)
		next(f_o)
		dico_mois = {}
		# comptage du nombre d'occurences par mois
		for line in f_o:
			if line[25][0:7] not in dico_mois and line[25] != "":
				dico_mois[line[25][0:7]] = 1
			elif line[25][0:7] in dico_mois and line[25] != "":
				dico_mois[line[25][0:7]] = dico_mois[line[25][0:7]] + 1
		liste_mois = []
		dico_annee = {"01": 31, "02": 29, "03": 31, "04": 30, "05": 31, "06":30, "07": 31, "08": 31, "09": 30, "10": 31, "11": 30, "12": 31}
		#remplissage des jours vides
		for cle in dico_mois:
			if cle[5:7] in dico_annee:
				for jour in range(1, dico_annee[cle[5:7]]):
					liste_mois.append([cle + "/"+ str(jour), dico_mois[cle]])
		#création du dataframe pour Altair
		data_mois = pd.DataFrame(liste_mois)
		data_mois.columns = ["Date_inventaire", 'occurences']
		data_mois['Date_inventaire'] = pd.to_datetime(data_mois['Date_inventaire'], format="%Y/%m")

	chart = classe_graphiques.generate_temporels_bar(data_mois, "Mois et jour")
	return chart.to_json()

#@app.route("/graphiques/cumulatifs")
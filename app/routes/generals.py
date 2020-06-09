from flask import render_template, flash, redirect, request
from ..app import app
import altair
from ..models.graphiques import classe_graphiques
import pandas as pd

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
	data = pd.read_csv(f"./app/statics/data/inventaire_complet.csv")
	data["Date_inventaire"] = pd.to_datetime(data["Date_inventaire"], format="%Y/%m/%d")
	#ajout colonne occurences
	data["occurences"] = 1

	# Group data by date
	general = data.groupby("Date_inventaire", as_index=False).sum()
	
	chart = classe_graphiques.generate_temporels(general, "Mois et jour")
	return chart.to_json()

#@app.route("/graphiques/cumulatifs")
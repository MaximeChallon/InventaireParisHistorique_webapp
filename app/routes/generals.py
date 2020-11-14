from flask import render_template, redirect, url_for, request, flash, send_from_directory
from flask_login import current_user, login_user, logout_user, login_required
from ..app import app, db, login_manager, mail
from ..models.graphiques import classe_graphiques
import pandas as pd
from ..models.donnees import Classe_db
from ..models.users import Classe_utilisateurs
from ..models.formulaires import Chart_rythme_catalogage_form, Reset_password_form, Forgot_form
from ..models.mails import Classe_mails
from ..constantes import MAIL_USERNAME
from werkzeug.security import generate_password_hash
import json
import requests
import os
#from ..utils import get_latlg_addresses

# routes dans l'ordre:
#/
#/cartographie
#/json_carto
#/graphiques
#/graphiques/temporels
#/inscription
#/connexion
#/deconnexion
#/reset_password
#/get_latlg_addresses
#/catalogue

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'statics/img'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route("/", methods=['post','get'])
def accueil():
	"""
	Route de la page d'accueil
	:return: template
	"""
	compteur_catalogueurs = Classe_utilisateurs.query.count()
	compteur_photos_inventoriees = Classe_db.query.count()
	compteur_photos_geolocalisees = db.session.query(Classe_db).filter(Classe_db.Latitude_x != "").count()

	flash("[Nouveautés du mois de novembre] Catalogue dans l'onglet Données; Filtres sur la cartographie; Géolocalisation automatique lors du catalogage", "info")
	return render_template("pages/accueil.html",
						   compteur_catalogueurs=compteur_catalogueurs,
						   compteur_photos_inventoriees=compteur_photos_inventoriees,
						   compteur_photos_geolocalisees=compteur_photos_geolocalisees)


#les routes cratographie et json_carto vont ensemble: la première affiche le html, la seconde fournit à Ajax de la première le JSON nécessaire
@app.route("/cartographie")
def cartographie():
	"""
	Route de la page de la cartographie
	:return: template
	"""
	return render_template("pages/cartographie.html")


@app.route("/json_carto")
def json_carto():
	"""
	Permet de renvoyer le JSON de la cartographie
	:return: JSON
	"""
	arrondissement = request.args.get("_Arrondissement", '')
	try:
		mot = request.args.get("_Mot", '').upper()
	except:
		mot = request.args.get("_Mot", '')
	try:
		site = request.args.get("_Site", '').upper()
	except:
		site = request.args.get("_Site", '')
	try:
		photographe = request.args.get("_Photographe", '').upper()
	except:
		photographe = request.args.get("_Photographe", '')
	date = request.args.get("_Date", '')

	where_clause = ""

	if arrondissement != '' or mot != '' or site !='' or photographe != '' or date != '':
		where_clause = " where "
		i = 0
		statut_arrondissement = 0
		statut_mot = 0
		statut_photographe = 0
		statut_site = 0
		statut_date = 0
		if arrondissement != "" and i ==0:
			where_clause = where_clause + "Arrondissement  in ('"+ str(arrondissement) + "')"
			i += 1
			statut_arrondissement = 1
		if arrondissement != "" and i !=0 and statut_arrondissement == 0:
			where_clause = where_clause + " and Arrondissement  in ('"+ str(arrondissement) + "')"
		if mot != "" and i ==0:
			where_clause = where_clause + "(Mot_cle1  in ('"+ str(mot) + "') or Mot_cle2 in ('"+ str(mot) + "') or Mot_cle3 in ('"+ str(mot) + "') or Mot_cle4 in ('"+ str(mot) + "') or Mot_cle5 in ('"+ str(mot) + "') or Mot_cle6 in ('"+ str(mot) + "'))"
			i += 1
			statut_mot = 1
		if mot != "" and i !=0 and statut_mot == 0:
			where_clause = where_clause + " and (Mot_cle1  in ('"+ str(mot) + "') or Mot_cle2 in ('"+ str(mot) + "') or Mot_cle3 in ('"+ str(mot) + "') or Mot_cle4 in ('"+ str(mot) + "') or Mot_cle5 in ('"+ str(mot) + "') or Mot_cle6 in ('"+ str(mot) + "'))"
		if photographe != "" and i ==0:
			where_clause = where_clause + "Photographe  like '"+ str(photographe) + "%'"
			i += 1
			statut_photographe = 1
		if photographe != "" and i !=0 and statut_photographe == 0:
			where_clause = where_clause + " and Photographe  like '" + str(photographe) + "%'"
		if site != "" and i ==0:
			where_clause = where_clause + "Nom_site  like '"+ str(site) + "%'"
			i += 1
			statut_site = 1
		if site != "" and i !=0 and statut_site == 0:
			where_clause = where_clause + " and Nom_site  like '" + str(site) + "%'"
		if date != "" and i ==0:
			where_clause = where_clause + "Date_prise_vue  like '"+ str(date) + "%'"
			i += 1
			statut_date = 1
		if date != "" and i !=0 and statut_date == 0:
			where_clause = where_clause + " and Date_prise_vue  like '" + str(date) + "%'"

	requete = """select * from Classe_db""" + where_clause
	results = db.session.execute(requete).fetchall()

	data = {}
	i=0
	for photo in results:
		data[str(i)] = {"N_inventaire": str(photo[0]),
		 "Rue": photo[1],
		 "N_rue": photo[2],
		 "Nom_site": photo[3],
		 "Arrondissement": str(photo[4]),
		 "Ville": photo[5],
		 "Latitude_x": photo[6],
		 "Longitude_y": photo[7],
		 "Support": photo[8],
		 "Couleur": photo[9],
		 "Taille": photo[10],
		 "Date_prise_vue": photo[11],
		 "Photographe": photo[12],
		 "Mot_cle1": photo[17],
		 "Mot_cle2": photo[18],
		 "Mot_cle3": photo[19],
		 "Mot_cle4": photo[20],
		 "Mot_cle5": photo[21],
		 "Mot_cle6": photo[22],
		 "Cote_base": photo[23],
		 "Cote_classement": photo[24]
		 }
		i += 1

	json_array = {"data": data}
	return json_array


# les routes suivantes vont ensemble: la première gère l'affichage des graphiques, les autres contiennent seulement le JSOn nécessaire aux graphiques
@app.route("/rythme_catalogage", methods=['get', 'post'])
def rythme_catalogage(visuel="line", dates='general_au_jour'):
	"""
	Permet de visualiser les graphiques des données
	:param visuel: type de graphique (bar ou line)
	:param dates: type de données à utiliser (mensuelles ou quotidiennes)
	:return: template
	"""
	# récupération des données d'URL
	visuel = request.args.get("visuel", 'line')
	dates = request.args.get("dates", 'general_au_jour')

	# construction des graphiques en fonction des paramètres donnés
	form = Chart_rythme_catalogage_form()
	if form.validate_on_submit():
		if form.visuel.data == "bar":
			return redirect(url_for('rythme_catalogage', visuel=form.visuel.data, dates=form.dates.data))
		else:
			return redirect(url_for('rythme_catalogage', visuel=form.visuel.data, dates=form.dates.data))

	return render_template("pages/graphique_rythme_catalogage.html", visuel=visuel, dates=dates, form=form)


@app.route("/graphiques/temporels_rythme_catalogage")
def temporels_rythme_catalogage(visuel='line', dates='general_au_jour'):
	"""
	Retourne le JSON du graphique demandé
	:param visuel: type de graphique (bar ou line)
	:param dates: type de données à utiliser (mensuelles ou quotidiennes)
	:return: JSON
	"""
	# récupération des paramètres d'URL
	visuel = request.args.get("visuel", 'line')
	dates = request.args.get("amp;dates", 'general_au_jour')

	# récupération des dates de chaque photographie
	liste = [[x.Date_inventaire] for x in Classe_db.query.all()]

	# construction des graphiques selon le type de date
	if dates == 'general_au_jour':
		data_jour = pd.DataFrame(liste, columns=["Date_inventaire"])
		data_jour["Date_inventaire"] = pd.to_datetime(data_jour["Date_inventaire"], format="%Y/%m/%d")
		data_jour["occurences"] = 1
		general_au_jour = data_jour.groupby("Date_inventaire", as_index=False).sum()
		donnees = general_au_jour

	elif dates == 'data_mois':
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
		donnees = data_mois

	if visuel == "bar":
		chart = classe_graphiques.generate_temporels_bar(donnees, "Mois et jour")
	elif visuel == "line":
		chart = classe_graphiques.generate_temporels_line(donnees, "Mois et jour")

	return chart.to_json()


@app.route("/graphiques/repartition_arrondissements")
def repartition_arrondissements():
	return render_template("pages/repartition_arrondissements.html")


@app.route("/graphiques/geojson_arrondissements")
def geojson_arrondissements():
	# ouverture du fichier geojson des arrondissements pour lui ajouter le nombre de photos du PH dans ses propriétés
	# "/home/ParisHistoriqueInventaire/InventaireParisHistorique/app/statics/data/arrondissements.geojson"
	with open("InventaireParisHistorique/app/statics/data/arrondissements.geojson", "r") as jsonfile:
		data = json.load(jsonfile)
		for ardt in data["features"]:
			nombre_photos = Classe_db.query.filter(Classe_db.Arrondissement == str(ardt["properties"]["c_ar"])).count()
			ardt["properties"]["nombre_photos"] = nombre_photos
	return json.dumps(data)


# routes de gestion des utilisateurs, et de modification des mots de passe
@app.route("/inscription", methods=["GET", "POST"])
@login_required
def inscription():
	"""
	Permet l'inscription d'un utilisateur et le hashage du mot de passe (pas mis dans la navbar pour éviter les utilisateurs non désirables)
	:return: template
	"""
	# Si on est en POST, cela veut dire que le formulaire a été envoyé
	if request.method == "POST":
		statut, donnees = Classe_utilisateurs.creer(
			nom=request.form.get("nom", None),
			prenom=request.form.get("prenom", None),
			mail=request.form.get("mail", None),
            motdepasse=request.form.get("motdepasse", None)
        )
		if statut is True:
			flash("Inscription réussie, veuillez vous connecter", "info")
			return redirect("/")
		else:
			flash("L'inscription a échoué, veuillez recommencer", "warning")
			return render_template("pages/inscription.html")
	else:
		flash("L'inscription a échoué, veuillez recommencer", "warning")
		return render_template("pages/inscription.html")


@app.route("/connexion", methods=["POST", "GET"])
def connexion():
	"""
	Permet la connexion de l'utilisateur
	:return:  template
	"""
	if current_user.is_authenticated is True:
		flash("Vous êtes déjà connecté", "info")
		return redirect("/")
	if request.method == "POST":
		utilisateur = Classe_utilisateurs.identification(
			nom=request.form.get("nom", None),
            motdepasse=request.form.get("motdepasse", None)
		)
		if utilisateur:
			login_user(utilisateur)
			flash("Vous êtes maintenant connecté", "info")
			return redirect("/")
		else:
			flash("La connexion a échoué, veuillez recommencer", "warning")
			return render_template("pages/connexion.html")

	return render_template("pages/connexion.html")
login_manager.login_view = 'connexion'


@app.route("/deconnexion", methods=["POST", "GET"])
def deconnexion():
	"""
	Permet la déconnexion de l'utilisateur
	:return: template
	"""
	if current_user.is_authenticated is True:
		logout_user()
		flash("Vous êtes maintenant déconnecté", "info")
	return redirect("/")


@app.route("/reset_password", methods=['get', 'post'])
def forgot_password():
	"""
	Permet de demander un lien de changement de mot de passe
	:return:template
	"""
	if current_user.is_authenticated:
		flash("Vous êtes connecté", "info")
		return redirect(url_for('accueil'))
	form = Forgot_form()
	if form.validate_on_submit():
		try:
			user = Classe_utilisateurs.query.filter_by(mail=form.email.data).first()
			Classe_mails.send_reset_email(user)
			msg = "Un mail a été envoyé à l'adresse " + form.email.data + " avec les instructions pour changer de mot de passe.\nPensez à vérifier les spams.\nLe lien n'est valable que 30 minutes.\nL'expéditeur est "+MAIL_USERNAME
			flash(msg, "info")
			return redirect(url_for('accueil'))
		except:
			flash("Une erreur est survenue lors de l'envoi du mail", "warning")
			return redirect("forgot_password")
	return render_template("pages/forgot_password.html", form=form)


@app.route("/reset_password/<token>", methods=['get', 'post'])
def reset_token(token):
	"""
	Permet de changer le mot de passe à partir du token reçu par mail
	:param token: chaîne de caractère limitée dans le temps
	:return: template
	"""
	if current_user.is_authenticated:
		flash("Vous êtes connecté", "info")
		return redirect(url_for('accueil'))
	user = Classe_utilisateurs.verify_reset_token(token)
	if user is None:
		flash("Lien invalide ou expiré.", "warning")
		return redirect(url_for('forgot_password'))
	form = Reset_password_form()
	if form.validate_on_submit():
		user.password_hash = generate_password_hash(form.current_password.data)
		db.session.commit()
		flash("Le mot de passe a bien été modifié", "info")
		return redirect(url_for('connexion'))
	return render_template("pages/reset_token.html", form=form)

"""
@app.route("/get_latlg_adresses")
@login_required
def get_latlg_adresses():
	fonctions = get_latlg_addresses.run()
	return fonctions
"""


@app.route("/catalogue", methods=['GET', 'POST'])
def catalogue():
	return render_template("pages/catalogue.html")


@app.route("/get_json_final",methods=['GET', 'POST'])
def get_json_final():
	photos = []
	i = 0
	for photo in Classe_db.query.all():
		photos.append(photo.to_json_catalogue())
		i += 1
	json_final = (json.dumps(photos))
	return json_final


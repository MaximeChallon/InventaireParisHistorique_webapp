from ..app import app, db
from flask_login import login_required
from flask import url_for, render_template
from ..models.formulaires import Catalogage_form

#SQL creation table ds db users
"""CREATE TABLE `catalogage` (
	`N_inventaire`	INTEGER NOT NULL,
	`Rue`	TEXT,
	`N_rue`	TEXT,
	`Nom_site`	TEXT,
	`Arrondissement`	TEXT,
	`Ville`	TEXT,
	`Departement`	INTEGER,
	`Latitude_x`	TEXT,
	`Longitude_y`	TEXT,
	`Support`	TEXT,
	`Couleur`	TEXT,
	`Taille`	TEXT,
	`Date_prise_vue`	TEXT,
	`Photographe`	TEXT,
	`Droits`	TEXT,
	`Mention_don`	TEXT,
	`Mention_collection`	TEXT,
	`Date_construction`	TEXT,
	`Architecte`	TEXT,
	`Classement_MH`	TEXT,
	`Legende`	TEXT,
	`Generalite_architecture`	TEXT,
	`Mot_cle1`	TEXT,
	`Mot_cle2`	TEXT,
	`Mot_cle3`	TEXT,
	`Mot_cle4`	TEXT,
	`Mot_cle5`	TEXT,
	`Mot_cle6`	TEXT,
	`Autre_adresse`	TEXT,
	`Notes`	TEXT,
	`Cote_base`	TEXT,
	`Cote_classement`	TEXT,
	`Date_inventaire`	TEXT,
	`Auteur`	TEXT,
	`exporte`	INTEGER NOT NULL
);"""


#créer un espace personnel pour chaque membre sur le type de Admin, où il peut:
#voir ce qu'il a catalogué
#exporté les données remplies entre tel jour et tel jour
#envoyer directement à l'adresse de la photothèque le csv final de catalogage

#supprimer les photos 30 jours après l'envoi ou l'export pour ne pas surcharger la base

#proposer le gps lors du catalogage avec une recherche sur cette api: https://api-adresse.data.gouv.fr/search/?q=34+poissonniers+rue+des+paris .
#les résultats semblent bons: les intégrer dans une minimap pour que l'utilisateur clique sur oui ou non

@app.route("/espace_personnel/<nom_user>/cataloguer", methods=['GET', 'POST'])
@login_required
def cataloguer(nom_user):
    form = Catalogage_form()
    if form.validate_on_submit():
        pass
    return render_template("pages/cataloguer.html", form=form)

#@app.route("/espace_personnel/<nom_user>/exporter")
#@login_required
#def exporter(nom_user):

#@app.route("/espace_personnel/<nom_user>/enregistrements_recents")
#@login_required
#def enregistrements_recents(nom_user):
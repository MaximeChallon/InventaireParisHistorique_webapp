from ..app import app, db
from flask_login import login_required, current_user
from flask import url_for, render_template, flash, redirect
from ..models.formulaires import Catalogage_form
from ..models.users import Classe_catalogage

#SQL creation table ds db users
"""CREATE TABLE catalogage (
	N_inventaire_index  INTEGER PRIMARY KEY NOT NULL,
	N_inventaire	INTEGER NOT NULL,
	Rue	TEXT,
	N_rue	TEXT,
	Nom_site	TEXT,
	Arrondissement	TEXT,
	Ville	TEXT,
	Departement	INTEGER,
	Latitude_x	TEXT,
	Longitude_y	TEXT,
	Support	TEXT,
	Couleur	TEXT,
	Taille	TEXT,
	Date_prise_vue	TEXT,
	Photographe	TEXT,
	Droits	TEXT,
	Mention_don	TEXT,
	Mention_collection	TEXT,
	Date_construction	TEXT,
	Architecte	TEXT,
	Classement_MH	TEXT,
	Legende	TEXT,
	Generalite_architecture	TEXT,
	Mot_cle1	TEXT,
	Mot_cle2	TEXT,
	Mot_cle3	TEXT,
	Mot_cle4	TEXT,
	Mot_cle5	TEXT,
	Mot_cle6	TEXT,
	Autre_adresse	TEXT,
	Notes	TEXT,
	Cote_base	TEXT,
	Cote_classement	TEXT,
	Date_inventaire	TEXT,
	Auteur	TEXT,
	exporte	INTEGER NOT NULL
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
        mots_cles = form.Mot_cle.data
        i=0
        j=6-len(mots_cles)
        if len(mots_cles)<6:
            while i!=j:
                mots_cles.append("")
                i += 1
        nouvelle_photo = Classe_catalogage(
            N_inventaire_index=form.N_inventaire.data,
            N_inventaire=form.N_inventaire.data,
            Rue=form.Rue.data,
            N_rue=form.N_rue.data,
            Nom_site=form.Nom_site.data,
            Arrondissement = form.Arrondissement.data,
            Ville = form.Ville.data,
            Departement = form.Departement.data,
            Latitude_x = form.Latitude_x.data,
            Longitude_y = form.Longitude_y.data,
            Support = form.Support.data,
            Couleur = form.Couleur.data,
            Taille = form.Taille.data,
            Date_prise_vue = form.Date_prise_vue.data,
            Photographe = form.Photographe.data,
            Droits = form.Droits.data,
            Mention_don = form.Mention_don.data,
            Mention_collection = form.Mention_collection.data,
            Date_construction = form.Date_construction.data,
            Architecte = form.Architecte.data,
            Classement_MH = form.Classement_MH.data,
            Legende = form.Legende.data,
            Generalite_architecture = form.Generalite_architecture.data,
            Mot_cle1 = form.Mot_cle.data[0],
            Mot_cle2=form.Mot_cle.data[1],
            Mot_cle3=form.Mot_cle.data[2],
            Mot_cle4=form.Mot_cle.data[3],
            Mot_cle5=form.Mot_cle.data[4],
            Mot_cle6=form.Mot_cle.data[5],
            Autre_adresse = form.Autre_adresse.data,
            Notes = form.Notes.data,
            Cote_base = form.Cote_base.data,
            Auteur = current_user.id_utilisateur
        )
        db.session.add(nouvelle_photo)
        db.session.commit()
        flash("Photographie correctement enregistrée", "info")
    return render_template("pages/cataloguer.html", form=form)

#@app.route("/espace_personnel/<nom_user>/exporter")
#@login_required
#def exporter(nom_user):

#@app.route("/espace_personnel/<nom_user>/enregistrements_recents")
#@login_required
#def enregistrements_recents(nom_user):
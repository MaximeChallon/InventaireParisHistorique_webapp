from ..app import app, db
from flask_login import login_required, current_user
from flask import url_for, render_template, flash, redirect, request
from ..models.formulaires import Catalogage_form
from ..models.users import Classe_catalogage
from ..models.export import Classe_export
from ..constantes import *

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


@app.route("/espace_personnel/cataloguer", methods=['GET', 'POST'])
@login_required
def cataloguer():
    """
    Permet de remplir le formulaire de catalogage et d'inscrire les données dans la base users.sqlite et la table catalogage
    :param nom_user: nom de famille de l'utilisateur
    :return: template
    """
    form = Catalogage_form()
    if form.validate_on_submit():
        nouvelle_photo = Classe_catalogage(
            N_inventaire_index=form.N_inventaire.data,
            N_inventaire=form.N_inventaire.data,
            Rue=form.Rue.data,
            N_rue=form.N_rue.data,
            Nom_site=form.Nom_site.data,
            Arrondissement = form.Arrondissement.data,
            Ville = form.Ville.data,
            Departement = int(form.Departement.data),
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
            Mot_cle1 = form.Mot_cle1.data,
            Mot_cle2=form.Mot_cle2.data,
            Mot_cle3=form.Mot_cle3.data,
            Mot_cle4=form.Mot_cle4.data,
            Mot_cle5=form.Mot_cle5.data,
            Mot_cle6=form.Mot_cle6.data,
            Autre_adresse = form.Autre_adresse.data,
            Notes = form.Notes.data,
            Cote_base = form.Cote_base.data,
            Auteur = current_user.id_utilisateur
        )
        try:
            db.session.add(nouvelle_photo)
            db.session.commit()
            flash("Photographie correctement enregistrée", "info")
            return redirect(url_for('cataloguer'))
        except:
            flash("Echec de l'enregistrement, veuillez vérifier que les champs sont remplis correctement", "warning")
    return render_template("pages/cataloguer.html", form=form)


@app.route("/espace_personnel/exporter", methods=['get', 'post'])
@login_required
def exporter():
    """
    Fonction d'exportation des données générées par l'utilisateur, dans l'intervalle de dexu numéros d'inventaire
    :param nom_user: nom de l'utiliateur
    :return: template
    """
    if request.method == "POST":
        num_debut = request.form.get("num_debut", None)
        num_fin = request.form.get("num_fin", None)
        envoyer = request.form.get("envoyer", "non")
        copie = request.form.get("copie", "non")
        flash("L'export débute", "info")
        Classe_export.exporter_csv(num_debut=num_debut, num_fin=num_fin, envoyer=envoyer, copie=copie)
    return render_template("pages/exporter.html")


@app.route("/espace_personnel/enregistrements_recents")
@login_required
def enregistrements_recents():
    """
    Permet de visualiser les photos récemment cataloguées par l'utilisateur
    :param nom_user:  nom de famille de l'utilisateur
    :return: template
    """
    photos = Classe_catalogage.query.filter_by(auteur=current_user).all()
    return render_template("pages/enregistrements_recents.html", photos=photos)


@app.route("/espace_personnel/editer_photographie/<id_photo>", methods=['GET', "POST"])
@login_required
def editer_photographie( id_photo):
    """
    Permet d'éditer une photographie avec un pré-remplissage des champs
    :param nom_user: nom de famille de l'utilisateur
    :param id_photo: numéro d'inventaire de la photographie à éditer
    :return: template
    """
    form = Catalogage_form()
    # récupération des données de la photo, 404 si elle n'existe pas
    photo = Classe_catalogage.query.get_or_404(id_photo)
    # traitement des 6 mots clés et remplisage par des chaînes vides s'ils ne sont pas remplis
    mots_cles = form.Mot_cle.data
    i = 0
    j = 6 - len(mots_cles)
    if len(mots_cles) < 6:
        while i != j:
            mots_cles.append("")
            i += 1
    # lors de la validation du formulaire, intégration des données dans la base
    if form.validate_on_submit():
        photo.N_inventaire_index = form.N_inventaire.data
        photo.N_inventaire = form.N_inventaire.data
        photo.Rue = form.Rue.data
        photo.N_rue = form.N_rue.data
        photo.Nom_site = form.Nom_site.data
        photo.Arrondissement = form.Arrondissement.data
        photo.Ville = form.Ville.data
        photo.Departement = form.Departement.data
        photo.Latitude_x = form.Latitude_x.data
        photo.Longitude_y = form.Longitude_y.data
        photo.Support = form.Support.data
        photo.Couleur = form.Couleur.data
        photo.Taille = form.Taille.data
        photo.Date_prise_vue = form.Date_prise_vue.data
        photo.Photographe = form.Photographe.data
        photo.Droits = form.Droits.data
        photo.Mention_don = form.Mention_don.data
        photo.Mention_collection = form.Mention_collection.data
        photo.Date_construction = form.Date_construction.data
        photo.Architecte = form.Architecte.data
        photo.Classement_MH = form.Classement_MH.data
        photo.Legende = form.Legende.data
        photo.Generalite_architecture = form.Generalite_architecture.data
        photo.Mot_cle1 = form.Mot_cle1.data
        photo.Mot_cle2 = form.Mot_cle2.data
        photo.Mot_cle3 = form.Mot_cle3.data
        photo.Mot_cle4 = form.Mot_cle4.data
        photo.Mot_cle5 = form.Mot_cle5.data
        photo.Mot_cle6 = form.Mot_cle6.data
        photo.Autre_adresse = form.Autre_adresse.data
        photo.Notes = form.Notes.data
        photo.Cote_base = form.Cote_base.data
        photo.Auteur = current_user.id_utilisateur
        db.session.add(photo)
        db.session.commit()
        flash("La photographie a bien été mise à jour", "info")
    # pré-remplissage du formulaire avec les données existantes
    form.N_inventaire.data = photo.N_inventaire_index
    form.N_inventaire.data = photo.N_inventaire
    form.Rue.data = photo.Rue
    form.N_rue.data = photo.N_rue
    form.Nom_site.data = photo.Nom_site
    form.Arrondissement.data = photo.Arrondissement
    form.Ville.data = photo.Ville
    form.Departement.data = photo.Departement
    form.Latitude_x.data = photo.Latitude_x
    form.Longitude_y.data = photo.Longitude_y
    form.Support.data = photo.Support
    form.Couleur.data = photo.Couleur
    form.Taille.data = photo.Taille
    form.Date_prise_vue.data = photo.Date_prise_vue
    form.Photographe.data = photo.Photographe
    form.Droits.data = photo.Droits
    form.Mention_don.data = photo.Mention_don
    form.Mention_collection.data = photo.Mention_collection
    form.Date_construction.data = photo.Date_construction
    form.Architecte.data = photo.Architecte
    form.Classement_MH.data = photo.Classement_MH
    form.Legende.data = photo.Legende
    form.Generalite_architecture.data = photo.Generalite_architecture
    form.Mot_cle1.data = photo.Mot_cle1
    form.Mot_cle2.data = photo.Mot_cle2
    form.Mot_cle3.data = photo.Mot_cle3
    form.Mot_cle4.data = photo.Mot_cle4
    form.Mot_cle5.data = photo.Mot_cle5
    form.Mot_cle6.data = photo.Mot_cle6
    form.Autre_adresse.data = photo.Autre_adresse
    form.Notes.data = photo.Notes
    form.Cote_base.data = photo.Cote_base
    return render_template("pages/editer_photographie.html", form=form)
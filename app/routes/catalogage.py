from ..app import app, db
from flask_login import login_required, current_user
from flask import url_for, render_template, flash, redirect, abort, send_file, request
import pandas as pd
import io
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


@app.route("/espace_personnel/<nom_user>/cataloguer", methods=['GET', 'POST'])
@login_required
def cataloguer(nom_user):
    """
    Permet de remplir le formulaire de catalogage et d'inscrire les données dans la base users.sqlite et la table catalogage
    :param nom_user: nom de famille de l'utilisateur
    :return: template
    """
    form = Catalogage_form()
    if form.validate_on_submit():
        # gestion des  mots-clés, remplissage par des chaînes vides si les  champs ne sont pas remplis
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


@app.route("/espace_personnel/<nom_user>/exporter", methods=['get', 'post'])
@login_required
def exporter(nom_user):
    """
    Fonction d'exportation des données générées par l'utilisateur, dans l'intervalle de dexu numéros d'inventaire
    :param nom_user: nom de l'utiliateur
    :return: template
    """
    if request.method == "POST":
        num_debut = request.form.get("num_debut", None)
        num_fin = request.form.get("num_fin", None)
        flash("Le téléchargement débute", "info")
        return redirect(url_for('exporter_csv', nom_user=nom_user, num_debut=num_debut, num_fin=num_fin))
    return render_template("pages/exporter.html")


@app.route("/espace_personnel/<nom_user>/exporter/<num_debut>/<num_fin>")
@login_required
def exporter_csv(nom_user, num_debut, num_fin):
    """
    Permet d'exporter au format CSV les données remplies de l'utilisateur entre les numéros d'inventaire donnés en URL
    :param nom_user: nom de famille de l'utilisateur
    :param num_debut: numéro d'inventaire de début d'export
    :param num_fin: numéro d'inventaire de fin d'export
    :return: file
    """
    # initialisation du nombre de début d'incrémentation, et des listes d'accueil des données
    i = int(num_debut)
    liste_photos = []
    liste_finale=[]
    # pour chaque numéro d'inventaire donné, requête SQL puis vérification que l'auteur est bien le demandeur de l'export, puis export des données
    while i <= int(num_fin) and i>=int(num_debut):
        try:
            photo = Classe_catalogage.query.get(i)
            if photo and photo.auteur==current_user:
                liste_photo = []
                liste_photos.append(photo)
                liste_photo.append(photo.N_inventaire)
                liste_photo.append(photo.Rue)
                liste_photo.append(photo.N_rue)
                liste_photo.append(photo.Nom_site)
                liste_photo.append(photo.Arrondissement)
                liste_photo.append(photo.Ville)
                liste_photo.append(photo.Departement)
                liste_photo.append(photo.Latitude_x)
                liste_photo.append(photo.Longitude_y)
                liste_photo.append(photo.Support)
                liste_photo.append(photo.Couleur)
                liste_photo.append(photo.Taille)
                liste_photo.append(photo.Date_prise_vue)
                liste_photo.append(photo.Photographe)
                liste_photo.append(photo.Droits)
                liste_photo.append(photo.Mention_don)
                liste_photo.append(photo.Mention_collection)
                liste_photo.append(photo.Date_construction)
                liste_photo.append(photo.Architecte)
                liste_photo.append(photo.Classement_MH)
                liste_photo.append(photo.Legende)
                liste_photo.append(photo.Generalite_architecture)
                liste_photo.append(photo.Mot_cle1)
                liste_photo.append(photo.Mot_cle2)
                liste_photo.append(photo.Mot_cle3)
                liste_photo.append(photo.Mot_cle4)
                liste_photo.append(photo.Mot_cle5)
                liste_photo.append(photo.Mot_cle6)
                liste_photo.append(photo.Autre_adresse)
                liste_photo.append(photo.Notes)
                liste_photo.append(photo.Cote_base)
                liste_photo.append(photo.Cote_classement)
                liste_photo.append(photo.Date_inventaire)
                liste_photo.append(current_user.nom.upper())
                liste_finale.append(liste_photo)
        except:
            pass
        i+=1
    # passage de la liste_finale dans un dataframe Pandas
    dataframe = pd.DataFrame(liste_finale)
    proxyIO = io.StringIO()
    dataframe.to_csv(proxyIO, index=False, header=False, encoding="utf-8")
    # transformation du dataframe en fichier CSV
    mem = io.BytesIO()
    mem.write(proxyIO.getvalue().encode("utf-8"))
    mem.seek(0)

    envoi_fichier = send_file(
            mem,
            mimetype="text/csv",
            attachment_filename="inventaire" + num_debut + "-" + num_fin +".csv",
            as_attachment=True,
            cache_timeout=0,
        )

    return envoi_fichier

@app.route("/espace_personnel/<nom_user>/enregistrements_recents")
@login_required
def enregistrements_recents(nom_user):
    """
    Permet de visualiser les photos récemment cataloguées par l'utilisateur
    :param nom_user:  nom de famille de l'utilisateur
    :return: template
    """
    photos = Classe_catalogage.query.filter_by(auteur=current_user).all()
    return render_template("pages/enregistrements_recents.html", photos=photos)


@app.route("/espace_personnel/<nom_user>/editer_photographie/<id_photo>", methods=['GET', "POST"])
@login_required
def editer_photographie(nom_user, id_photo):
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
        photo.Mot_cle1 = form.Mot_cle.data[0]
        photo.Mot_cle2 = form.Mot_cle.data[1]
        photo.Mot_cle3 = form.Mot_cle.data[2]
        photo.Mot_cle4 = form.Mot_cle.data[3]
        photo.Mot_cle5 = form.Mot_cle.data[4]
        photo.Mot_cle6 = form.Mot_cle.data[5]
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
    form.Mot_cle.data[0] = photo.Mot_cle1
    form.Mot_cle.data[1] = photo.Mot_cle2
    form.Mot_cle.data[2] = photo.Mot_cle3
    form.Mot_cle.data[3] = photo.Mot_cle4
    form.Mot_cle.data[4] = photo.Mot_cle5
    form.Mot_cle.data[5] = photo.Mot_cle6
    form.Autre_adresse.data = photo.Autre_adresse
    form.Notes.data = photo.Notes
    form.Cote_base.data = photo.Cote_base
    return render_template("pages/editer_photographie.html", form=form)
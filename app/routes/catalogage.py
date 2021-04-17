from ..app import app, db
from flask_login import login_required, current_user
from flask import url_for, render_template, flash, redirect, request
from ..models.formulaires import Catalogage_form
from ..models.users import Classe_catalogage
from ..models.export import Classe_export
from ..constantes import *
import re

from ..models.actions import Actions

# SQL creation table ds db users
"""CREATE TABLE catalogage (
    N_inventaire_index  INTEGER PRIMARY KEY NOT NULL,
    N_inventaire    INTEGER NOT NULL,
    Rue    TEXT,
    N_rue    TEXT,
    Nom_site    TEXT,
    Arrondissement    TEXT,
    Ville    TEXT,
    Departement    INTEGER,
    Latitude_x    TEXT,
    Longitude_y    TEXT,
    Support    TEXT,
    Couleur    TEXT,
    Taille    TEXT,
    Date_prise_vue    TEXT,
    Photographe    TEXT,
    Droits    TEXT,
    Mention_don    TEXT,
    Mention_collection    TEXT,
    Date_construction    TEXT,
    Architecte    TEXT,
    Classement_MH    TEXT,
    Legende    TEXT,
    Generalite_architecture    TEXT,
    Mot_cle1    TEXT,
    Mot_cle2    TEXT,
    Mot_cle3    TEXT,
    Mot_cle4    TEXT,
    Mot_cle5    TEXT,
    Mot_cle6    TEXT,
    Autre_adresse    TEXT,
    Notes    TEXT,
    Cote_base    TEXT,
    Cote_classement    TEXT,
    Date_inventaire    TEXT,
    Auteur    TEXT,
    exporte    INTEGER NOT NULL
);"""


@app.route("/cotes", methods=["GET", "POST"])
@login_required
def cotes():
    if request.method == "POST":
        num_debut = request.form.get("num_debut", None)
        num_fin = request.form.get("num_fin", None)
        cote = request.form.get("cote", None)
        if num_fin is None:
            num_fin = num_debut
        i = int(num_debut)
        while i <= int(num_fin) and i >= int(num_debut):
            try:
                if (
                    db.session.execute(
                        "select * from cotes where N_inventaire = " + str(i)
                    ).fetchall()
                    == []
                ):
                    db.session.execute(
                        """insert into cotes values ("""
                        + str(i)
                        + ","
                        + str(i)
                        + ",'"
                        + str(cote)
                        + "','"
                        + str(current_user.nom)
                        + "'"
                        + """)"""
                    )
                    db.session.commit()
                else:
                    flash(str(i) + " possède déjà une cote", "info")
                    db.session.rollback()
            except Exception as e:
                print(e)
                db.session.rollback()
            i += 1
        last = db.session.execute(
            "select N_inventaire from cotes order by N_inventaire desc limit 1"
        ).fetchall()
        return render_template("pages/cotes.html", last=last)
    last = db.session.execute(
        "select N_inventaire from cotes order by N_inventaire desc limit 1"
    ).fetchall()
    return render_template("pages/cotes.html", last=last)


@app.route("/espace_personnel/cataloguer", methods=["GET", "POST"])
@login_required
def cataloguer():
    """
    Permet de remplir le formulaire de catalogage et d'inscrire les données dans la base users.sqlite et la table catalogage
    :param nom_user: nom de famille de l'utilisateur
    :return: template
    """
    form = Catalogage_form()
    if form.validate_on_submit():
        check_data_bool, check_data_message = Classe_catalogage.check_data(form)
        if check_data_bool == True:
            nouvelle_photo = Classe_catalogage(
                N_inventaire_index=form.N_inventaire.data,
                N_inventaire=form.N_inventaire.data,
                Rue=form.Rue.data,
                N_rue=form.N_rue.data,
                Nom_site=form.Nom_site.data,
                Arrondissement=form.Arrondissement.data,
                Ville=form.Ville.data,
                Departement=int(form.Departement.data),
                Latitude_x=form.Latitude_x.data,
                Longitude_y=form.Longitude_y.data,
                Support=form.Support.data,
                Couleur=form.Couleur.data,
                Taille=form.Taille.data,
                Date_prise_vue=form.Date_prise_vue.data,
                Photographe=form.Photographe.data,
                Droits=form.Droits.data,
                Mention_don=form.Mention_don.data,
                Mention_collection=form.Mention_collection.data,
                Date_construction=form.Date_construction.data,
                Architecte=form.Architecte.data,
                Classement_MH=form.Classement_MH.data,
                Legende=form.Legende.data,
                Generalite_architecture=form.Generalite_architecture.data,
                Mot_cle1=form.Mot_cle1.data,
                Mot_cle2=form.Mot_cle2.data,
                Mot_cle3=form.Mot_cle3.data,
                Mot_cle4=form.Mot_cle4.data,
                Mot_cle5=form.Mot_cle5.data,
                Mot_cle6=form.Mot_cle6.data,
                Autre_adresse=form.Autre_adresse.data,
                Notes=(
                    (
                        (
                            "[Numéro d'inventaire lié: "
                            + (str(form.N_inventaire_lie.data))
                            + "]"
                        )
                        if (
                            form.N_inventaire_lie.data != "0"
                            and form.N_inventaire_lie.data != None
                            and form.N_inventaire_lie.data != ""
                        )
                        else ""
                    )
                    + form.Notes.data
                ),
                Cote_base=form.Cote_base.data,
                Auteur=current_user.id_utilisateur,
            )
            if form.Dupliquer.data == True:
                try:
                    db.session.add(nouvelle_photo)
                    db.session.commit()
                    flash("Photographie correctement enregistrée", "info")
                    Msg, new_id = Actions.duplicate(
                        Classe_catalogage.query.get_or_404(form.N_inventaire.data)
                    )
                    flash(Msg, "info")
                    return redirect(url_for("editer_photographie", id_photo=new_id))
                except:
                    flash(
                        "Echec de l'enregistrement, veuillez vérifier que les champs sont remplis correctement",
                        "warning",
                    )
            else:
                try:
                    db.session.add(nouvelle_photo)
                    db.session.commit()
                    flash("Photographie correctement enregistrée", "info")
                    return redirect(url_for("cataloguer"))
                except:
                    flash(
                        "Echec de l'enregistrement, veuillez vérifier que les champs sont remplis correctement",
                        "warning",
                    )
        else:
            flash("Une ou plusieurs erreur(s) sont survenues: " + str(" ; ".join(check_data_message)), "warning")
            return render_template("pages/cataloguer.html", form=form)
    return render_template("pages/cataloguer.html", form=form)


@app.route("/espace_personnel/exporter", methods=["get", "post"])
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
        Classe_export.exporter_csv(
            num_debut=num_debut, num_fin=num_fin, envoyer=envoyer, copie=copie
        )
    return render_template("pages/exporter.html")


@app.route("/espace_personnel/enregistrements_recents")
@login_required
def enregistrements_recents():
    """
    Permet de visualiser les photos récemment cataloguées par l'utilisateur
    :param nom_user:  nom de famille de l'utilisateur
    :return: template
    """
    """
    Permet de renvoyer le JSON de la cartographie
    :return: JSON
    """
    arrondissement = request.args.get("_Arrondissement", "")
    try:
        mot = request.args.get("_Mot", "").upper()
    except:
        mot = request.args.get("_Mot", "")
    try:
        site = request.args.get("_Site", "").upper()
    except:
        site = request.args.get("_Site", "")
    try:
        photographe = request.args.get("_Photographe", "").upper()
    except:
        photographe = request.args.get("_Photographe", "")
    date = request.args.get("_Date", "")

    where_clause = ""

    if (
        arrondissement != ""
        or mot != ""
        or site != ""
        or photographe != ""
        or date != ""
    ):
        where_clause = " where "
        i = 0
        statut_arrondissement = 0
        statut_mot = 0
        statut_photographe = 0
        statut_site = 0
        statut_date = 0
        if arrondissement != "" and i == 0:
            if ";" not in arrondissement:
                where_clause = (
                    where_clause + "Arrondissement  in ('" + str(arrondissement) + "')"
                )
            else:
                arrondissements = arrondissement.split(";")
                requete = [
                    "Arrondissement  in ('" + str(arrdt) + "')"
                    for arrdt in arrondissements
                ]
                where_clause = where_clause + " or ".join(requete)
            i += 1
            statut_arrondissement = 1
        if arrondissement != "" and i != 0 and statut_arrondissement == 0:
            if ";" not in arrondissement:
                where_clause = (
                    where_clause + "Arrondissement  in ('" + str(arrondissement) + "')"
                )
            else:
                arrondissements = arrondissement.split(";")
                requete = [
                    "Arrondissement  in ('" + str(arrdt) + "')"
                    for arrdt in arrondissements
                ]
                where_clause = where_clause + " or ".join(requete)

        if mot != "" and i == 0:
            if ";" not in mot:
                where_clause = (
                    where_clause
                    + "(Mot_cle1  in ('"
                    + str(mot)
                    + "') or Mot_cle2 in ('"
                    + str(mot)
                    + "') or Mot_cle3 in ('"
                    + str(mot)
                    + "') or Mot_cle4 in ('"
                    + str(mot)
                    + "') or Mot_cle5 in ('"
                    + str(mot)
                    + "') or Mot_cle6 in ('"
                    + str(mot)
                    + "'))"
                )
            else:
                mots = mot.split(";")
                requete = [
                    "(Mot_cle1  in ('"
                    + str(un_mot)
                    + "') or Mot_cle2 in ('"
                    + str(un_mot)
                    + "') or Mot_cle3 in ('"
                    + str(un_mot)
                    + "') or Mot_cle4 in ('"
                    + str(un_mot)
                    + "') or Mot_cle5 in ('"
                    + str(un_mot)
                    + "') or Mot_cle6 in ('"
                    + str(un_mot)
                    + "'))"
                    for un_mot in mots
                ]
                where_clause = where_clause + " or ".join(requete)
            i += 1
            statut_mot = 1
        if mot != "" and i != 0 and statut_mot == 0:
            if ";" not in mot:
                where_clause = (
                    where_clause
                    + "(Mot_cle1  in ('"
                    + str(mot)
                    + "') or Mot_cle2 in ('"
                    + str(mot)
                    + "') or Mot_cle3 in ('"
                    + str(mot)
                    + "') or Mot_cle4 in ('"
                    + str(mot)
                    + "') or Mot_cle5 in ('"
                    + str(mot)
                    + "') or Mot_cle6 in ('"
                    + str(mot)
                    + "'))"
                )
            else:
                mots = mot.split(";")
                requete = [
                    "(Mot_cle1  in ('"
                    + str(un_mot)
                    + "') or Mot_cle2 in ('"
                    + str(un_mot)
                    + "') or Mot_cle3 in ('"
                    + str(un_mot)
                    + "') or Mot_cle4 in ('"
                    + str(un_mot)
                    + "') or Mot_cle5 in ('"
                    + str(un_mot)
                    + "') or Mot_cle6 in ('"
                    + str(un_mot)
                    + "'))"
                    for un_mot in mots
                ]
                where_clause = where_clause + " or ".join(requete)

        if photographe != "" and i == 0:
            where_clause = (
                where_clause + "Photographe  like '" + str(photographe) + "%'"
            )
            i += 1
            statut_photographe = 1
        if photographe != "" and i != 0 and statut_photographe == 0:
            where_clause = (
                where_clause + " and Photographe  like '" + str(photographe) + "%'"
            )

        if site != "" and i == 0:
            where_clause = where_clause + "Nom_site  like '" + str(site) + "%'"
            i += 1
            statut_site = 1
        if site != "" and i != 0 and statut_site == 0:
            where_clause = where_clause + " and Nom_site  like '" + str(site) + "%'"

        if date != "" and i == 0:
            if "-" not in date:
                where_clause = (
                    where_clause + "Date_prise_vue  like '" + str(date) + "%'"
                )
            else:
                dates = date.split("-")
                where_clause = (
                    where_clause
                    + "Date_prise_vue  >= '"
                    + str(dates[0])
                    + "'"
                    + " and Date_prise_vue  <= '"
                    + str(dates[1])
                    + "'"
                )
            i += 1
            statut_date = 1
        if date != "" and i != 0 and statut_date == 0:
            if "-" not in date:
                where_clause = (
                    where_clause + " and Date_prise_vue  like '" + str(date) + "%'"
                )
            else:
                dates = date.split("-")
                where_clause = (
                    where_clause
                    + "Date_prise_vue  >= '"
                    + str(dates[0])
                    + "'"
                    + " and Date_prise_vue  <= '"
                    + str(dates[1])
                    + "'"
                )

        if where_clause != "":
            requete = (
                """select * from catalogage"""
                + where_clause
                + " and Auteur == "
                + str(current_user.id_utilisateur)
            )
        else:
            requete = (
                """select * from catalogage"""
                + where_clause
                + " where Auteur == "
                + str(current_user.id_utilisateur)
            )
        photos = db.get_engine(bind="users").execute(requete).fetchall()
    else:
        photos = Classe_catalogage.query.filter_by(auteur=current_user).all()
    return render_template("pages/enregistrements_recents.html", photos=photos)


@app.route("/espace_personnel/editer_photographie/<id_photo>", methods=["GET", "POST"])
@login_required
def editer_photographie(id_photo):
    """
    Permet d'éditer une photographie avec un pré-remplissage des champs
    :param nom_user: nom de famille de l'utilisateur
    :param id_photo: numéro d'inventaire de la photographie à éditer
    :return: template
    """
    form = Catalogage_form()
    # récupération des données de la photo, 404 si elle n'existe pas
    photo = Classe_catalogage.query.get_or_404(id_photo)
    # lors de la validation du formulaire, intégration des données dans la base
    if form.validate_on_submit():
        if form.Delete.data == True:
            Msg, n_inv = Actions.delete(form.N_inventaire.data)
            flash(Msg, "info")
            return redirect(url_for("cataloguer"))
        check_data_bool, check_data_message = Classe_catalogage.check_data(form, check_id=False)
        if check_data_bool == True:
            photo.N_inventaire_index = form.N_inventaire.data
            photo.N_inventaire = form.N_inventaire.data
            photo.Rue = form.Rue.data
            photo.N_rue = form.N_rue.data
            photo.Nom_site = form.Nom_site.data
            photo.Arrondissement = form.Arrondissement.data
            photo.Ville = form.Ville.data
            photo.Departement = form.Departement.data
            photo.Latitude_x = str(form.Latitude_x.data)
            photo.Longitude_y = str(form.Longitude_y.data)
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
            photo.Notes = (
            ("[Numéro d'inventaire lié: " + (str(form.N_inventaire_lie.data)) + "]")
                if (
                    form.N_inventaire_lie.data != "0"
                    and form.N_inventaire_lie.data != None
                    and form.N_inventaire_lie.data != ""
                )
                else ""
            ) + form.Notes.data
            photo.Cote_base = form.Cote_base.data
            photo.Auteur = current_user.id_utilisateur
            db.session.add(photo)
            db.session.commit()
            flash("La photographie a bien été mise à jour", "info")


            if form.Dupliquer.data == True:
                try:
                    Msg, new_id = Actions.duplicate(
                        Classe_catalogage.query.get_or_404(form.N_inventaire.data)
                    )
                    flash(Msg, "info")
                    return redirect(url_for("editer_photographie", id_photo=new_id))
                except:
                    flash("Echec de la duplication", "warning")
            else:
                try:
                    return redirect(url_for("cataloguer"))
                except:
                    flash("Echec de la duplication", "warning")
            return redirect(url_for("cataloguer"))
        else:
            flash("Une ou plusieurs erreur(s) sont survenues: " + str(" ; ".join(check_data_message)), "warning")
            return render_template("pages/editer_photographie.html", form=form)
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
    form.N_inventaire_lie.data = (
        (re.sub("\].*", "", photo.Notes.replace("[Numéro d'inventaire lié: ", "")))
        if "[" in photo.Notes
        else "0"
    )
    form.Legende.data = photo.Legende
    form.Generalite_architecture.data = photo.Generalite_architecture
    form.Mot_cle1.data = photo.Mot_cle1
    form.Mot_cle2.data = photo.Mot_cle2
    form.Mot_cle3.data = photo.Mot_cle3
    form.Mot_cle4.data = photo.Mot_cle4
    form.Mot_cle5.data = photo.Mot_cle5
    form.Mot_cle6.data = photo.Mot_cle6
    form.Autre_adresse.data = photo.Autre_adresse
    form.Notes.data = re.sub("\[[^\]]+\]", "", photo.Notes)
    form.Cote_base.data = photo.Cote_base
    return render_template("pages/editer_photographie.html", form=form)


@app.route("/espace_personnel/dupliquer/<id_photo>", methods=["GET", "POST"])
@login_required
def dupliquer_photographie(id_photo):
    """Créé un doublon de la photographie en attribuant un numéro d'inventaire provisoire
    Renvoie à la page Editer_photographie quand la duplication est terminée"""
    old_model = Classe_catalogage.query.get_or_404(id_photo)
    Msg, new_id = Actions.duplicate(old_model)
    return redirect(url_for("editer_photographie", id_photo=new_id))


@app.route("/espace_personnel/supprimer/<id_photo>", methods=["GET", "POST"])
@login_required
def supprimer_photographie(id_photo):
    Msg, new_id = Actions.delete(id_photo)
    flash(Msg, "info")
    return redirect(url_for("enregistrements_recents"))
from flask_login import current_user
from flask import flash, Response
import io
from .users import Classe_catalogage
from .mails import Classe_mails
import csv
from ..constantes import *

class Classe_export():
    @staticmethod
    def exporter_csv(num_debut, num_fin, envoyer, copie):
        """
        Permet d'exporter au format CSV les données remplies de l'utilisateur entre les numéros d'inventaire donnés en URL
        :param nom_user: nom de famille de l'utilisateur
        :param num_debut: numéro d'inventaire de début d'export
        :param num_fin: numéro d'inventaire de fin d'export
        :return: file
        """
        # initialisation du nombre de début d'incrémentation, et des listes d'accueil des données
        i = int(num_debut)
        liste_globale = []
        # pour chaque numéro d'inventaire donné, requête SQL puis vérification que l'auteur est bien le demandeur de l'export, puis export des données
        while i <= int(num_fin) and i >= int(num_debut):
            try:
                photo = Classe_catalogage.query.get(i)
                if photo and photo.auteur == current_user:
                    liste_photo = []
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
                    item = "|".join(map(str, liste_photo))
                    liste_globale.append(item)
            except:
                pass
            i += 1

        destinataires = [MAIL_USERNAME, MAIL_TRAVAIL_PHOTOTHEQUE]

        if envoyer == "oui":
            Classe_mails.envoyer_export(liste_globale, destinataires)
            flash("Mail correctement envoyé", "info")
        elif copie == "oui":
            destinataires.append(current_user.mail)
            Classe_mails.envoyer_export(liste_globale, destinataires)
            flash("Mail correctement envoyé", "info")
        elif copie == "oui" and envoyer == "oui":
            destinataires.append(current_user.mail)
            Classe_mails.envoyer_export(liste_globale, destinataires)
            flash("Mail correctement envoyé", "info")
        else:
            flash("Veuillez sélectionner une action", "warning")
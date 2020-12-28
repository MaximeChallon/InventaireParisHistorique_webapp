from ..app import db, app

from flask_login import current_user

from ..models.users import Classe_catalogage


class Actions():
	def duplicate(old_model):
		print(old_model)
		n_inv = int(str(db.get_engine(app, 'users').execute("""select N_inventaire 
			from catalogage order by N_inventaire desc""").fetchall()[0]).replace('"', "").replace("(", "").replace(",","").replace(")","")) + 1

		new_model = Classe_catalogage(
            N_inventaire_index=n_inv,
            N_inventaire=n_inv,
            Rue=old_model.Rue,
            N_rue=old_model.N_rue,
            Nom_site=old_model.Nom_site,
            Arrondissement = old_model.Arrondissement,
            Ville = old_model.Ville,
            Departement = int(old_model.Departement),
            Latitude_x = old_model.Latitude_x,
            Longitude_y = old_model.Longitude_y,
            Support = old_model.Support,
            Couleur = old_model.Couleur,
            Taille = old_model.Taille,
            Date_prise_vue = old_model.Date_prise_vue,
            Photographe = old_model.Photographe,
            Droits = old_model.Droits,
            Mention_don = old_model.Mention_don,
            Mention_collection = old_model.Mention_collection,
            Date_construction = old_model.Date_construction,
            Architecte = old_model.Architecte,
            Classement_MH = old_model.Classement_MH,
            Legende = old_model.Legende,
            Generalite_architecture = old_model.Generalite_architecture,
            Mot_cle1 = old_model.Mot_cle1,
            Mot_cle2=old_model.Mot_cle2,
            Mot_cle3=old_model.Mot_cle3,
            Mot_cle4=old_model.Mot_cle4,
            Mot_cle5=old_model.Mot_cle5,
            Mot_cle6=old_model.Mot_cle6,
            Autre_adresse = old_model.Autre_adresse,
            Notes = old_model.Notes,
            Cote_base = old_model.Cote_base,
            Auteur = current_user.id_utilisateur
            )

		try:
			db.session.add(new_model)
			db.session.commit()
			Msg = "Duplication réussie: nouveau numéro d'inventaire provisoire " + str(n_inv)
			return Msg, n_inv
		except Exception as e:
			Msg = "Une erreur est survenue lors de l'insertion: " + str(e)
			return Msg

from flask_admin import Admin, expose, BaseView
from ..app import db, admin, app
from flask_admin.contrib.sqla import ModelView
from ..models.users import Classe_utilisateurs, Classe_catalogage
from flask_login import current_user
from flask import abort, flash, redirect, url_for
from flask_admin.contrib.sqla.filters import FilterEqual


class Classe_admin_controller(ModelView):
    column_filters = (Classe_catalogage.Date_inventaire, Classe_utilisateurs.nom, Classe_catalogage.Rue, Classe_catalogage.Nom_site)
    column_searchable_list = (Classe_catalogage.Date_inventaire, Classe_utilisateurs.nom, Classe_catalogage.Rue, Classe_catalogage.Nom_site)

    # classe de contrôle de l'authentification de l'utilisateur pour avoir accès au panneau d'administration
    def is_accessible(self):
        """
        Contrôle de l'authentification de l'utilisateur pour lui donner accès au panneau d'administration
        :return: True ou erreur 404
        """
        if current_user.is_admin == True:
            return current_user.is_authenticated
        else:
            return abort(404)
    def not_auth(self):
        """
        Interdiction d'accès au panneau d'administration
        :return: template
        """
        flash("Vous n'êtes pas autorisé à accéder à cette page.")
        return redirect(url_for('accueil'))

admin.add_view(Classe_admin_controller(Classe_utilisateurs, db.session))
admin.add_view(Classe_admin_controller(Classe_catalogage, db.session))
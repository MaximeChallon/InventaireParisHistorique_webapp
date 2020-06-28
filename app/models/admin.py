from flask_admin import Admin, expose, BaseView
from ..app import app, db, admin, login_manager
from flask_admin.contrib.sqla import ModelView
from ..models.users import Classe_utilisateurs, Classe_catalogage
from flask_login import current_user
from flask import abort, flash, redirect, url_for


class Classe_admin_controller(ModelView):
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
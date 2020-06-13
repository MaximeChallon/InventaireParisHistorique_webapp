from flask_admin import Admin, expose, BaseView
from ..app import app, db, admin, login_manager
from flask_admin.contrib.sqla import ModelView
from ..models.users import Classe_utilisateurs
from flask_login import current_user
from flask import abort


class Classe_admin_controller(ModelView):
    def is_accessible(self):
        if current_user.is_admin == True:
            return current_user.is_authenticated
        else:
            return abort(404)
    def not_auth(self):
        return "Vous n'êtes pas autorisé à accéder à cette page."

admin.add_view(Classe_admin_controller(Classe_utilisateurs, db.session))
from ..app import db, admin, app
from ..models.users import Classe_utilisateurs, Classe_catalogage
from ..models.actions import Actions
from ..models.donnees import cotes

from flask_login import current_user

from flask import abort, current_app, flash, redirect, request, url_for

from flask_admin.helpers import get_redirect_target, flash_errors
from flask_admin.model.helpers import get_mdict_item_or_list
from flask_admin.contrib.sqla.filters import FilterEqual
from flask_admin.model.template import LinkRowAction
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, expose, BaseView, AdminIndexView

from gettext import gettext

class Classe_admin_controller(ModelView):
    column_filters = (Classe_catalogage.Date_inventaire, Classe_utilisateurs.nom, Classe_catalogage.Rue, Classe_catalogage.Nom_site)
    column_searchable_list = (Classe_catalogage.Date_inventaire, Classe_utilisateurs.nom, Classe_catalogage.Rue, Classe_catalogage.Nom_site)
    column_extra_row_actions=[
        LinkRowAction(
            icon_class='fa fa-repeat glyphicon icon-repeat',
            url='duplicate?id={row_id}',
            title="Duplicate Row"
        ),
    ]

    list_template = 'admin_templates/list.html'
    create_template = 'admin_templates/create.html'
    edit_template = 'admin_templates/edit.html'

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

    @expose('/duplicate/')
    def duplicate_record(self):
        """Make a duplicate of the current record"""
        
        view_args = self._get_list_extra_args()

        return_url = get_redirect_target() or self.get_url('.index_view')

        if not self.can_create:
            return redirect(return_url)

        id_ = get_mdict_item_or_list(request.args, 'id')
        if id_ is None:
            flash(gettext("Impossible de trouver le numéro d'inventaire demandé"), 'error')
            return redirect(return_url)

        old_model = self.get_one(id_)
        if old_model is None:
            flash(gettext('Aucun enregistrement existant'), 'error')
            return redirect(return_url)

        Msg, n_inv = Actions.duplicate(old_model)
        flash(gettext(Msg), 'success')

        return redirect(return_url)

admin.add_view(Classe_admin_controller(Classe_utilisateurs, db.session))
admin.add_view(Classe_admin_controller(Classe_catalogage, db.session))
admin.add_view(Classe_admin_controller(cotes, db.session))
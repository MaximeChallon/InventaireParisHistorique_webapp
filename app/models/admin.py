from ..app import db, admin, app
from ..models.users import Classe_utilisateurs, Classe_catalogage

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

        # Grab parameters from URL
        view_args = self._get_list_extra_args()

        # Duplicate current record
        return_url = get_redirect_target() or self.get_url('.index_view')

        if not self.can_create:
            return redirect(return_url)

        id_ = get_mdict_item_or_list(request.args, 'id')
        if id_ is None:
            flash(gettext("Can't find the 'id' for the record to be duplicated."), 'error')
            return redirect(return_url)

        old_model = self.get_one(id_)
        #print(old_model.Rue)
        if old_model is None:
            flash(gettext('Record does not exist.'), 'error')
            return redirect(return_url)
        n_inv = db.session.execute("select N_inventaire from Classe_catalogage order by N_inventaire desc").fetchall()[0]
        print(n_inv)
        # Make a clone of the old model, without the primary key
        new_model = Classe_catalogage(
            N_inventaire_index=old_model.N_inventaire,
            N_inventaire=old_model.N_inventaire,
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
        print(new_model.N_inventaire_index)

        # Add duplicate record to the database
        db.session.add(old_model)
        db.session.commit()
        flash(gettext("You have successfully duplicated that record."), 'success')

        return redirect(return_url)

admin.add_view(Classe_admin_controller(Classe_utilisateurs, db.session))
admin.add_view(Classe_admin_controller(Classe_catalogage, db.session))
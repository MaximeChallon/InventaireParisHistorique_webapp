from ..app import app, db
from flask_login import login_required, current_user
from flask import url_for, render_template, flash, redirect, request
from ..models.formulaires import ModifierInformationsPersonnelles
from ..models.users import Classe_catalogage
from ..models.export import Classe_export
from ..constantes import *

@app.route("/espace_personnel/mon_profil", methods=['GET', 'POST'])
@login_required
def mon_profil():
    form = ModifierInformationsPersonnelles()
    form.Prenom.data = current_user.prenom
    form.Nom.data = current_user.nom
    form.Mail.data = current_user.mail
    if form.validate_on_submit():
        pass
    #return
    return render_template("pages/profil.html", form=form)
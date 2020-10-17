from ..app import app, db
from flask_login import login_required, current_user
from flask import render_template, redirect, url_for, flash
from ..models.formulaires import ModifierInformationsPersonnelles
from ..models.donnees import Classe_db
from ..models.users import Classe_utilisateurs, Classe_catalogage

@app.route("/espace_personnel/mon_profil", methods=['GET', 'POST'])
@login_required
def mon_profil():
    compteur_photos_ok = Classe_db.query.filter_by(Auteur=current_user.nom.upper()).count()
    compteur_photos_attente = db.session.query(Classe_catalogage).filter(Classe_catalogage.Auteur==current_user.id_utilisateur).count()
    form = ModifierInformationsPersonnelles()
    if form.validate_on_submit():
        current_user.nom = form.Nom.data
        current_user.prenom = form.Prenom.data
        current_user.mail = form.Mail.data
        try:
            db.session.commit()
            flash("Informations modifiées", "info")
            return redirect(url_for('mon_profil'))
        except:
            flash("Une erreur est survenue. Veuillez nous excuser.", "warning")
        return redirect(url_for("mon_profil"))
    form.Prenom.data = current_user.prenom
    form.Nom.data = current_user.nom
    form.Mail.data = current_user.mail
    return render_template("pages/profil.html", form=form,
                           compteur_photos_ok=compteur_photos_ok,
                           compteur_photos_attente=compteur_photos_attente)
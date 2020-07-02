from flask import url_for, render_template, flash, redirect
from flask_login import login_required, current_user
from ..app import app
from ..models.formulaires import CataloguerContactForm
from ..models.mails import Classe_mails

@app.route("/espace_personnel/<nom_user>/cataloguer/contact", methods=['get', 'post'])
@login_required
def cataloguer_contact(nom_user):
    """
    Permet d'envoyer un mail à l'adinistrateur
    :param nom_user: nom de famille de l'utilisateur
    :return: template
    """
    form = CataloguerContactForm()
    if form.validate_on_submit():
        Classe_mails.send_cataloguer_contact_mail(user=current_user,
                                                  numero_inventaire=form.Numero_inventaire.data,
                                                  objet=form.Objet.data,
                                                  message=form.Message.data,
                                                  copie=form.Copie.data)
        flash("Mail envoyé avec succès", "info")
        return url_for("cataloguer", nom_user=current_user.nom)
    return render_template("pages/cataloguer_contact.html", form=form)

@app.route("/backup")
def backup():
    Classe_mails.daily_db_backup()
    return redirect(url_for("accueil"))
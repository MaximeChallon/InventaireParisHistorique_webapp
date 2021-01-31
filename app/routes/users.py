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

    # utiliser plotly faire les graphiques de l'issue 62
    mots_cles = db.session.execute("""select Mot_cle1, count(*) from Classe_db where Auteur  = '""" +
        current_user.nom.upper() + """' and Mot_cle1 is not null and Mot_cle1 != ''
group by Mot_cle1
        union
        select Mot_cle2, count(*) from Classe_db where Auteur  = '""" +
        current_user.nom.upper() + """' and Mot_cle2 is not null and Mot_cle2 != ''
group by Mot_cle2
        union
        select Mot_cle3, count(*) from Classe_db where Auteur  = '""" +
        current_user.nom.upper() + """' and Mot_cle3 is not null and Mot_cle3 != ''
group by Mot_cle3
        union
        select Mot_cle4, count(*) from Classe_db where Auteur  = '""" +
        current_user.nom.upper() + """' and Mot_cle4 is not null and Mot_cle4 != ''
group by Mot_cle4
        union
        select Mot_cle5, count(*) from Classe_db where Auteur  = '""" +
        current_user.nom.upper() + """' and Mot_cle5 is not null and Mot_cle5 != ''
group by Mot_cle5
        union
        select Mot_cle6, count(*) from Classe_db where Auteur  = '""" +
        current_user.nom.upper() + """' and Mot_cle6 is not null and Mot_cle6 != ''
group by Mot_cle6""").fetchall()
    dico = {}
    for item in mots_cles:
        if item[0] not in  dico:
            dico[item[0]] = item[1]
        if item[0] in dico:
            dico[item[0]] = dico[item[0]] + item[1]
    liste_mots = []
    liste_valeurs = []
    for entree in dico:
        liste_mots.append(entree)
        liste_valeurs.append(dico[entree])
    liste_finale_mots = [liste_mots, liste_valeurs]

    return render_template("pages/profil.html", form=form,
                           compteur_photos_ok=compteur_photos_ok,
                           compteur_photos_attente=compteur_photos_attente,
                           liste_mots_cles=liste_finale_mots)
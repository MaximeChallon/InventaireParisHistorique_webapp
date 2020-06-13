from ..app import db, login_manager, admin
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Classe_utilisateurs(db.Model, UserMixin):
    __tablename__ = "utilisateurs"
    __bind_key__ = "users"
    id_utilisateur = db.Column(db.Integer, primary_key=True, autoincrement=True)
    prenom = db.Column(db.String(64))
    nom = db.Column(db.String(64))
    password_hash = db.Column(db.String(240))
    mail = db.Column(db.String(120))
    is_admin = db.Column(db.Boolean, default=False)

    @staticmethod
    def identification(nom, motdepasse):
        utilisateur = Classe_utilisateurs.query.filter(Classe_utilisateurs.nom == nom).first()
        if utilisateur and check_password_hash(utilisateur.password_hash, motdepasse):
            return utilisateur
        return None

    @staticmethod
    def creer(nom, prenom, mail, motdepasse):
        erreurs = []
        if not nom:
            erreurs.append("Le login fourni est vide")
        if not prenom:
            erreurs.append("L'email fourni est vide")
        if not mail:
            erreurs.append("L'email fourni est vide")
        if not motdepasse or len(motdepasse) < 6:
            erreurs.append("Le mot de passe fourni est vide ou trop court")

        uniques = Classe_utilisateurs.query.filter(
            db.or_(Classe_utilisateurs.nom == nom, Classe_utilisateurs.prenom == prenom)
        ).count()
        if uniques > 0:
            erreurs.append("L'email ou le login sont déjà inscrits dans notre base de données")
        print(erreurs)
        if len(erreurs) > 0:
            return False, erreurs
        utilisateur = Classe_utilisateurs(
            prenom=prenom,
            nom=nom,
            mail=mail,
            password_hash=generate_password_hash(motdepasse)
        )
        try:
            db.session.add(utilisateur)
            db.session.commit()
            return True, utilisateur
        except Exception as erreur:
            return False, [str(erreur)]

    def get_id(self):
        return self.id_utilisateur


@login_manager.user_loader
def get_user_by_id(id):
    return Classe_utilisateurs.query.get(int(id))


from ..models.admin import Classe_admin_controller
from ..app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Classe_utilisateurs(db.Model, UserMixin):
    __tablename__ = "utilisateurs"
    __bind_key__ = "users"
    id_utilisateur = db.Column(db.Integer, primary_key=True, autoincrement=True)
    prenom = db.Column(db.String(64))
    nom = db.Column(db.String(64))
    password_hash = db.Column(db.String(240))

    @staticmethod
    def identification(nom, motdepasse):
        utilisateur = Classe_utilisateurs.query.filter(Classe_utilisateurs.nom == nom).first()
        if utilisateur and check_password_hash(utilisateur.password_hash, motdepasse):
            return utilisateur
        return None

    @staticmethod
    def creer(nom, prenom, motdepasse):
        erreurs = []
        if not nom:
            erreurs.append("Le login fourni est vide")
        if not prenom:
            erreurs.append("L'email fourni est vide")
        if not motdepasse or len(motdepasse) < 6:
            erreurs.append("Le mot de passe fourni est vide ou trop court")

        # On vérifie que personne n'a utilisé cet email ou ce login
        uniques = Classe_utilisateurs.query.filter(
            db.or_(Classe_utilisateurs.nom == nom, Classe_utilisateurs.prenom == prenom)
        ).count()
        if uniques > 0:
            erreurs.append("L'email ou le login sont déjà inscrits dans notre base de données")

        # Si on a au moins une erreur
        if len(erreurs) > 0:
            return False, erreurs

        # On crée un utilisateur
        utilisateur = Classe_utilisateurs(
            prenom=prenom,
            nom=nom,
            password_hash=generate_password_hash(motdepasse)
        )

        try:
            # On l'ajoute au transport vers la base de données
            db.session.add(utilisateur)
            # On envoie le paquet
            db.session.commit()

            # On renvoie l'utilisateur
            return True, utilisateur
        except Exception as erreur:
            print(erreurs)
            return False, [str(erreur)]

    def get_id(self):
        return self.id_utilisateur


@login_manager.user_loader
def get_user_by_id(id):
    return Classe_utilisateurs.query.get(int(id))
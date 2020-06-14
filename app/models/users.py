from ..app import db, login_manager, admin
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from ..constantes import SECRET_KEY

class Classe_utilisateurs(db.Model, UserMixin):
    __tablename__ = "utilisateurs"
    __bind_key__ = "users"
    id_utilisateur = db.Column(db.Integer, primary_key=True, autoincrement=True)
    prenom = db.Column(db.String(64))
    nom = db.Column(db.String(64))
    password_hash = db.Column(db.String(240))
    mail = db.Column(db.String(120))
    is_admin = db.Column(db.Boolean, default=False)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(SECRET_KEY, expires_sec)
        return s.dumps({'user_id': self.id_utilisateur}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(SECRET_KEY)
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return Classe_utilisateurs.query.get(user_id)


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


class Classe_catalogage(db.Model, UserMixin):
    __tablename__ = "catalogage"
    __bind_key__ = "users"
    N_inventaire = db.Column(db.Integer, primary=True, autoincrement=False)
    Rue = db.Column(db.String(64))
    N_rue = db.Column(db.String(64))
    Nom_site = db.Column(db.String(128))
    Arrondissement = db.Column(db.Integer)
    Ville = db.Column(db.String(64))
    Departement = db.Column(db.Integer)
    Latitude_x = db.Column(db.String(64))
    Longitude_y = db.Column(db.String(64))
    Support = db.Column(db.String(64))
    Couleur = db.Column(db.String(64))
    Taille = db.Column(db.String(64))
    Date_prise_vue = db.Column(db.String(64))
    Photographe = db.Column(db.String(64))
    Droits = db.Column(db.String(64))
    Mention_don = db.Column(db.String(64))
    Mention_collection = db.Column(db.String(64))
    Date_construction = db.Column(db.String(64))
    Architecte = db.Column(db.String(64))
    Classement_MH = db.Column(db.String(64))
    Legende = db.Column(db.String(512))
    Generalite_architecture = db.Column(db.String(64))
    Mot_cle1 = db.Column(db.String(24))
    Mot_cle2 = db.Column(db.String(24))
    Mot_cle3 = db.Column(db.String(24))
    Mot_cle4 = db.Column(db.String(24))
    Mot_cle5 = db.Column(db.String(24))
    Mot_cle6 = db.Column(db.String(24))
    Autre_adresse = db.Column(db.String(64))
    Notes = db.Column(db.String(512))
    Cote_base = db.Column(db.String(24))
    Cote_classement = db.Column(db.String(24))
    Date_inventaire = db.Column(db.String(48))
    Auteur = db.Column(db.Integer)
    exporte = db.Column(db.Integer)


@login_manager.user_loader
def get_user_by_id(id):
    return Classe_utilisateurs.query.get(int(id))


from ..models.admin import Classe_admin_controller
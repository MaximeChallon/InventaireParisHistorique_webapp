from ..app import db

class Classe_utilisateurs(db.Model):
    __tablename__ = "utilisateurs"
    __bind_key__ = "users"
    id_utilisateur = db.Column(db.Integer, primary_key=True, autoincrement=True)
    prenom = db.Column(db.String(64))
    nom = db.Column(db.String(64))
    password_hash = db.Column(db.String(240))
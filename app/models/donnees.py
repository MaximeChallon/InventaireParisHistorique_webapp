from ..app import db

class Classe_db(db.Model):
    # table de db contenant les métadonnées des photographies inventoriées
    N_inventaire = db.Column(db.Integer, primary_key=True)
    Rue = db.Column(db.String(120))
    N_rue = db.Column(db.String(120))
    Nom_site = db.Column(db.String(120))
    Arrondissement = db.Column(db.Integer)
    Ville = db.Column(db.String(120))
    Latitude_x = db.Column(db.String(120))
    Longitude_y = db.Column(db.String(120))
    Support = db.Column(db.String(120))
    Couleur = db.Column(db.String(120))
    Taille = db.Column(db.String(120))
    Date_prise_vue = db.Column(db.String(120))
    Photographe = db.Column(db.String(120))
    Date_construction = db.Column(db.String(120))
    Architecte = db.Column(db.String(120))
    Classement_MH = db.Column(db.String(120))
    Generalite_architecture = db.Column(db.String(120))
    Mot_cle1 = db.Column(db.String(120))
    Mot_cle2 = db.Column(db.String(120))
    Mot_cle3 = db.Column(db.String(120))
    Mot_cle4 = db.Column(db.String(120))
    Mot_cle5 = db.Column(db.String(120))
    Mot_cle6 = db.Column(db.String(120))
    Cote_base = db.Column(db.String(120))
    Cote_classement = db.Column(db.String(120))
    Date_inventaire = db.Column(db.String(120))

    def to_json(self):
        """
        Transforme les données extraites en JSON
        :return: dictionnaire
        :rtype: dict
        """
        return {"N_inventaire" : str(self.N_inventaire),
                "Rue": self.Rue,
                "N_rue": self.N_rue,
                "Nom_site": self.Nom_site,
                "Arrondissement": str(self.Arrondissement),
                "Ville": self.Ville,
                "Latitude_x": self.Latitude_x,
                "Longitude_y": self.Longitude_y,
                "Support": self.Support,
                "Couleur": self.Couleur,
                "Taille": self.Taille,
                "Date_prise_vue": self.Date_prise_vue,
                "Photographe": self.Photographe,
                "Mot_cle1": self.Mot_cle1,
                "Mot_cle2": self.Mot_cle2,
                "Mot_cle3": self.Mot_cle3,
                "Mot_cle4": self.Mot_cle4,
                "Mot_cle5": self.Mot_cle5,
                "Mot_cle6": self.Mot_cle6,
                "Cote_base": self.Cote_base,
                "Cote_classement": self.Cote_classement
                }
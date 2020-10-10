from wtforms import RadioField, SubmitField, TextAreaField, BooleanField, StringField, validators, PasswordField, SelectField, IntegerField, SelectMultipleField
from flask_wtf import FlaskForm
from .users import Classe_utilisateurs
from ..constantes import RUE, NOM_SITE, VILLE, CLASSEMENT_MH, MOT_CLE, GENERALITE_ARHITECTURE, PHOTOGRAPHE, SUPPORT, DROITS, COULEUR, COLLECTION

# classes contenant les formulaires utilisés dans l'application

class Chart_rythme_catalogage_form(FlaskForm):
    visuel = RadioField('Visuel', choices=[('line', 'En ligne'), ('bar', 'En barres')])
    dates = RadioField('Dates', choices=[('general_au_jour', 'Jour par jour'), ('data_mois', 'Mois par mois')])
    submit = SubmitField('Voir')

class Forgot_form(FlaskForm):
    email = StringField('Email Address', [validators.DataRequired(), validators.Length(min=6, max=75), validators.Email()])
    submit = SubmitField('Envoyer')

    def validate_email(self, email):
        """
        Permet de vréifier la présence d'une adresse email dasns la base de données des utilisateurs
        :param email: chaîne de caractères de l'email
        :type email: str
        :return: bool
        """
        user = Classe_utilisateurs.query.filter_by(mail=email.data)
        if user is None:
            raise AssertionError("Aucun compte avec cette adresse mail")


class Reset_password_form(FlaskForm):
    current_password = PasswordField("Mot de passe", [validators.DataRequired(), validators.Length(min=6, max=40)])
    confirm_password = PasswordField("Mot de passe", [validators.DataRequired(), validators.Length(min=6, max=40),
                                      validators.EqualTo('current_password')])
    submit = SubmitField('Enregistrer')

class Catalogage_form(FlaskForm):
    N_inventaire = IntegerField("Numéro d'inventaire", [validators.DataRequired()])
    Rue = SelectField("Rue", choices=RUE, default="")
    N_rue = StringField("Numéro de rue", default="")
    Nom_site = SelectField("Rue", choices=NOM_SITE, default="")
    Arrondissement = StringField("Arrondissement", [validators.Length(min=0, max=2, message="Le champ Arrondissement doit contenir deux chiffres.")], default="")
    Ville = SelectField("Rue", choices=VILLE, default=['PARIS', 'PARIS'])
    Departement = IntegerField("Code postal (2 premiers chiffres)", default=75)
    Latitude_x = StringField("Latitude", default="")
    Longitude_y = StringField("Longitude", default="")
    Support = SelectField("Support", choices=SUPPORT, default="")
    Couleur = SelectField("Couleur", choices=COULEUR, default="")
    Taille = StringField("Taille", default="")
    Date_prise_vue = StringField("Date de prise de vue", default="")
    Photographe = SelectField("Photographe", choices=PHOTOGRAPHE, default="INCONNU")
    Droits = SelectField("Droits", choices=DROITS, default="INCONNU")
    Mention_don = SelectField("Don", choices=PHOTOGRAPHE, default="INCONNU")
    Mention_collection = SelectField("Collection", choices=COLLECTION, default="")
    Date_construction = StringField("Date de construction", default="")
    Architecte = StringField("Architecte", default="")
    Classement_MH = SelectField("Classement MH", choices=CLASSEMENT_MH, default="INCONNU")
    Legende = TextAreaField("Date de prise de vue", default="", render_kw={"rows": 6, "cols": 40})
    Generalite_architecture = SelectField("Généralité architecture", choices=GENERALITE_ARHITECTURE, default="PRIVEE")
    Mot_cle1 = SelectField(choices = MOT_CLE, default = ['', ''])
    Mot_cle2 = SelectField(choices=MOT_CLE, default=['', ''])
    Mot_cle3 = SelectField(choices=MOT_CLE, default=['', ''])
    Mot_cle4 = SelectField(choices=MOT_CLE, default=['', ''])
    Mot_cle5 = SelectField(choices=MOT_CLE, default=['', ''])
    Mot_cle6 = SelectField(choices=MOT_CLE, default=['', ''])
    Autre_adresse = StringField("Autre adresse", default="")
    Notes = TextAreaField("Notes", default="", render_kw={"rows": 6, "cols": 100})
    Cote_base = StringField("Cote de la base", default="")

    submit = SubmitField('Enregistrer')

class CataloguerContactForm(FlaskForm):
    Numero_inventaire = IntegerField("Numéro d'inventaire",  [validators.DataRequired()])
    Objet = StringField("Objet", [validators.DataRequired()])
    Message = TextAreaField("Message", [validators.DataRequired()])
    Copie = BooleanField("Envoyer une copie à mon adresse mail ?")
    submit = SubmitField('Envoyer')
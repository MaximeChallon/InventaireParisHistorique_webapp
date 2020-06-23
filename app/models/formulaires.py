from wtforms import RadioField, SubmitField, StringField, validators, PasswordField, SelectField, IntegerField, SelectMultipleField
from flask_wtf import FlaskForm
from .users import Classe_utilisateurs
from ..constantes import RUE, NOM_SITE, VILLE, CLASSEMENT_MH, MOT_CLE, GENERALITE_ARHITECTURE, PHOTOGRAPHE, SUPPORT, DROITS, COULEUR, COLLECTION

# classes contenant les formulaires utilisés dans l'application

class Chart_form(FlaskForm):
    visuel = RadioField('Visuel', choices=[('line', 'En ligne'), ('bar', 'En barres')])
    dates = RadioField('Dates', choices=[('general_au_jour', 'Jour par jour'), ('data_mois', 'Mois par mois')])
    submit = SubmitField('Voir')

class Forgot_form(FlaskForm):
    email = StringField('Email Address', [validators.DataRequired(), validators.Length(min=6, max=35)], validators.Email())
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
    Rue = SelectField("Rue", choices=RUE)
    N_rue = StringField("Numéro de rue")
    Nom_site = SelectField("Rue", choices=NOM_SITE)
    Arrondissement = IntegerField("Arrondissement")
    Ville = SelectField("Rue", choices=VILLE)
    Departement = IntegerField("Code postal (2 premiers chiffres)")
    Latitude_x = StringField("Latitude")
    Longitude_y = StringField("Longitude")
    Support = SelectField("Support", choices=SUPPORT)
    Couleur = SelectField("Couleur", choices=COULEUR)
    Taille = StringField("Taille")
    Date_prise_vue = StringField("Date de prise de vue")
    Photographe = SelectField("Photographe", choices=PHOTOGRAPHE)
    Droits = SelectField("Droits", choices=DROITS)
    Mention_don = SelectField("Don", choices=PHOTOGRAPHE)
    Mention_collection = SelectField("Collection", choices=COLLECTION)
    Date_construction = StringField("Date de construction")
    Architecte = StringField("Architecte")
    Classement_MH = SelectField("Classement MH", choices=CLASSEMENT_MH)
    Legende = StringField("Date de prise de vue")
    Generalite_architecture = SelectField("Généralité architecture", choices=GENERALITE_ARHITECTURE)
    Mot_cle = SelectMultipleField(choices = MOT_CLE, default = ['', ''])
    Autre_adresse = StringField("Autre adresse")
    Notes = StringField("Notes")
    Cote_base = StringField("Cote de la base")

    submit = SubmitField('Enregistrer')
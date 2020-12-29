from wtforms import RadioField,widgets, SelectMultipleField, SubmitField, TextAreaField, BooleanField, StringField, validators, PasswordField, SelectField, IntegerField, SelectMultipleField
from flask_wtf import FlaskForm
from flask_login import current_user
from .users import Classe_utilisateurs
from ..app import db
from ..constantes import RUE, NOM_SITE, VILLE, CLASSEMENT_MH, MOT_CLE, GENERALITE_ARHITECTURE, PHOTOGRAPHE, SUPPORT, DROITS, COULEUR, COLLECTION
from collections import Counter

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

# classes contenant les formulaires utilisés dans l'application

#création de variables
ardt = [ (art[0], art[0]) for art in db.session.execute("""select distinct Arrondissement from Classe_db where Arrondissement != '' order by Arrondissement""")]

liste_mots_cles = []
for row in db.session.execute("""select Mot_cle1 , Mot_cle2 , Mot_cle3 , Mot_cle4 , Mot_cle5, Mot_cle6 
from Classe_db  
"""):
    if row is not None and row != '':
        if row[0] is not None and row[0] != '':
            liste_mots_cles.append(row[0])
        if row[1] is not None and row[1] != '':
            liste_mots_cles.append(row[1])
        if row[2] is not None and row[2] != '':
            liste_mots_cles.append(row[2])
        if row[3] is not None and row[3] != '':
            liste_mots_cles.append(row[3])
        if row[4] is not None and row[4] != '':
            liste_mots_cles.append(row[4])
        if row[5] is not None and row[5] != '':
            liste_mots_cles.append(row[5])
mots_cles = [(mc[0], mc[0] + " (" + str(mc[1]) + ")")for mc in Counter(liste_mots_cles).most_common()]

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

class Recherche_form(FlaskForm):
    Rue = StringField("Rue")
    Arrondissement = MultiCheckboxField('Arrondissement', choices=ardt)
    Mots_cles = MultiCheckboxField('Mots-clés', choices=mots_cles)

    submit = SubmitField('Envoyer')

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


class ModifierInformationsPersonnelles(FlaskForm):
    Prenom = StringField("Prénom")
    Nom = StringField("Nom", [validators.DataRequired()])
    Mail = StringField("Adresse e-mail", [validators.DataRequired()])
    submit = SubmitField('Modifier')
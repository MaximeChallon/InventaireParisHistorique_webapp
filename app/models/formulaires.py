from wtforms import RadioField, SubmitField, StringField, validators, PasswordField
from flask_wtf import FlaskForm
from .users import Classe_utilisateurs

class Chart_form(FlaskForm):
    visuel = RadioField('Visuel', choices=[('line', 'En ligne'), ('bar', 'En barres')])
    dates = RadioField('Dates', choices=[('general_au_jour', 'Jour par jour'), ('data_mois', 'Mois par mois')])
    submit = SubmitField('Voir')

class Forgot_form(FlaskForm):
    email = StringField('Email Address', [validators.DataRequired(), validators.Length(min=6, max=35)])
    submit = SubmitField('Envoyer')

    def validate_email(self, email):
        user = Classe_utilisateurs.query.filter_by(mail=email.data)
        if user is None:
            raise AssertionError("Aucun compte avec cette adresse mail")


class Reset_password_form(FlaskForm):
    current_password = PasswordField("Mot de passe", [validators.DataRequired(), validators.Length(min=6, max=40)])
    confirm_password = PasswordField("Mot de passe", [validators.DataRequired(), validators.Length(min=6, max=40),
                                      validators.EqualTo('current_password')])
    submit = SubmitField('Enregistrer')
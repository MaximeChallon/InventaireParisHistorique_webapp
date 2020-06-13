from wtforms import RadioField, SubmitField
from flask_wtf import FlaskForm

class Chart_form(FlaskForm):
    visuel = RadioField('Visuel', choices=[('line', 'En ligne'), ('bar', 'En barres')])
    dates = RadioField('Dates', choices=[('general_au_jour', 'Jour par jour'), ('data_mois', 'Mois par mois')])
    submit = SubmitField('Voir')

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin
from flask_mail import Mail
from .constantes import SECRET_KEY, MAIL_PASSWORD, MAIL_USERNAME, SQLALCHEMY_DATABASE_URI, SQLALCHEMY_BINDS
import os

chemin_actuel = os.path.dirname(os.path.abspath(__file__))
templates = os.path.join(chemin_actuel, "templates")
statics = os.path.join(chemin_actuel, "statics")

app = Flask(
    __name__,
    template_folder=templates,
    static_folder=statics
)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_BINDS'] = {'users': SQLALCHEMY_BINDS}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = SECRET_KEY

app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEBUG'] = True
app.config['MAIL_USERNAME'] = MAIL_USERNAME
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
mail = Mail(app)

admin = Admin(app)

login_manager = LoginManager(app)

from .routes import generals, catalogage, api, mails

def init_app():
    db.create_all()
    db.create_all(bind="users")
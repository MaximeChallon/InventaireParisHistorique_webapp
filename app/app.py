from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

chemin_actuel = os.path.dirname(os.path.abspath(__file__))
templates = os.path.join(chemin_actuel, "templates")
statics = os.path.join(chemin_actuel, "statics")

app = Flask(
    __name__,
    template_folder=templates,
    static_folder=statics
)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_BINDS'] = {'users': 'sqlite:///users.sqlite'}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'xxxxxxxx'

login_manager = LoginManager(app)

from .routes import generals

def init_app():
    db.create_all()
    db.create_all(bind="users")
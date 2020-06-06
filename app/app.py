from flask import Flask
import os

chemin_actuel = os.path.dirname(os.path.abspath(__file__))
templates = os.path.join(chemin_actuel, "templates")
statics = os.path.join(chemin_actuel, "statics")

app = Flask(
    __name__,
    template_folder=templates,
    static_folder=statics
)

from .routes import generals
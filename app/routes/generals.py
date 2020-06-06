from flask import render_template, flash, redirect, request
from ..app import app

@app.route("/")
def accueil():
    """ Route permettant l'affichage d'une page accueil
    """
    return render_template("pages/accueil.html")
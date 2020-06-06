from flask import render_template, flash, redirect, request

@app.route("/")
def accueil():
    """ Route permettant l'affichage d'une page accueil
    """
    return render_template("pages/accueil.html", nom="Accueil")
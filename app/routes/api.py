from ..app import app
from flask import render_template, request, url_for, jsonify
from urllib.parse import urlencode
from ..models.api import Classe_API
from..models.donnees import Classe_db
from ..constantes import CHEMIN_API
import re
from sqlalchemy import and_, or_
from AdresseParser import AdresseParser


def Json_404():
    response = jsonify({"erreur": "Requête impossible"})
    response.status_code = 404
    return response


@app.route(CHEMIN_API)
def api():
    """
    Route d'accueil de l'api
    :return: template
    """
    return render_template("pages/api.html")


@app.route(CHEMIN_API + "/photographie/numero_inventaire")
def single_photo_id():
    """
    Permet d'obtenir les données d'une photographie précise
    :return: JSON
    """
    recherche = request.args.get("q", None)
    page, results_per_page = Classe_API.check_n_p(1,1)
    query = Classe_db.query.filter(Classe_db.N_inventaire == int(recherche))

    try:
        resultats = query.paginate(page=page, per_page=results_per_page)
    except Exception:
        return Json_404()

    return jsonify(Classe_API.return_json(recherche, resultats, results_per_page))


@app.route(CHEMIN_API + "/photographie/numeros_inventaire")
def multiple_photo_id():
    """
    Permet d'obtenir les données des photograohies comprises dans l'intervalle donné en requête (le séparateur peut être tout sauf un chiffre)
    :return: JSON
    """
    recherche = request.args.get("q", None)
    page = request.args.get("n", 1)
    results_per_page = request.args.get("p", 10)

    page, results_per_page = Classe_API.check_n_p(page, results_per_page)

    _from = int(re.sub("[^0-9]+[0-9]+$", "", recherche))
    _to = int(re.sub("[0-9]+[^0-9]+", "", recherche))

    query = Classe_db.query.filter(Classe_db.N_inventaire.between(_from, _to))

    try:
        resultats = query.paginate(page=page, per_page=results_per_page)
    except Exception:
        return Json_404()

    response = Classe_API.return_json(recherche, resultats, results_per_page)
    return response


@app.route(CHEMIN_API+"/photographie/adresse")
def recherche_photo_adresse():
    """
    Recherche de photographie par adresse
    :return: JSON
    """
    recherche = request.args.get("q", None)
    page = request.args.get("p", 1)
    results_per_page = request.args.get("n", 10)

    page, results_per_page = Classe_API.check_n_p(page, results_per_page)

    # récupération de l'adresse parsée
    adresse_parser = AdresseParser()
    N_rue = str(adresse_parser.parse(recherche)["numero"])
    Rue = adresse_parser.parse(recherche)["rue"]["nom"]

    if recherche and N_rue != "-1":
        query = Classe_db.query.filter(and_(
            Classe_db.Rue.like("%{}%".format(Rue)), Classe_db.N_rue.like(N_rue))
        )
    elif recherche and N_rue == "-1":
        query = Classe_db.query.filter(
            Classe_db.Rue.like("%{}%".format(Rue))
        )
    else:
        query = Classe_db.query

    try:
        resultats = query.paginate(page=page, per_page=results_per_page)
    except Exception:
        return Json_404()

    response = jsonify(Classe_API.return_json(recherche, resultats, results_per_page))
    return response


@app.route(CHEMIN_API + "/photographie/mot_cle")
def recherche_photo_mot_cle():
    """
    Recherche de photographie par mot clé
    :return: JSON
    """
    recherche = request.args.get("q", None)
    page = request.args.get("p", 1)
    results_per_page = request.args.get("n", 10)

    page, results_per_page = Classe_API.check_n_p(page, results_per_page)

    mot_cle = recherche.upper()

    if recherche:
        query = Classe_db.query.filter(or_(
            Classe_db.Mot_cle1.like("%{}%".format(mot_cle)),
            Classe_db.Mot_cle2.like("%{}%".format(mot_cle)),
            Classe_db.Mot_cle3.like("%{}%".format(mot_cle)),
            Classe_db.Mot_cle4.like("%{}%".format(mot_cle)),
            Classe_db.Mot_cle5.like("%{}%".format(mot_cle)),
            Classe_db.Mot_cle6.like("%{}%".format(mot_cle)))
        )
    else:
        query = Classe_db.query

    try:
        resultats = query.paginate(page=page, per_page=results_per_page)
    except Exception:
        return Json_404()

    response = jsonify(Classe_API.return_json(recherche, resultats, results_per_page))
    return response
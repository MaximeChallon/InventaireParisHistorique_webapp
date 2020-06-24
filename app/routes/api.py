from ..app import app, db
from flask import render_template, request, url_for, jsonify
from urllib.parse import urlencode
from flask_login import login_required
from..models.donnees import Classe_db
from ..constantes import CHEMIN_API
import re
from address_parser import Parser
from sqlalchemy import and_, or_


def Json_404():
    response = jsonify({"erreur": "Requête impossible"})
    response.status_code = 404
    return response


def extract_adresse(requete):
    """
    Permet d'extraire l'adresse' de la requête de l'utilisateur
    :param requete: requête faite dans l'api
    :return: str
    """
    parser = Parser()
    adr = parser.parse(requete)
    return adr


@app.route(CHEMIN_API + "/photographie/numero_inventaire/<photo_id>")
@login_required
def single_photo_id(photo_id):
    """
    Permet d'obtenir les données d'une photographie précise
    :param photo_id: numéro d'inventaire de la photo
    :return: dict
    """
    try:
        query = Classe_db.query.get(photo_id)
        dict_json = {"data": {str(query.N_inventaire) : query.to_json()}
        }
        return jsonify(dict_json)
    except:
        return Json_404()


@app.route(CHEMIN_API+"/photographie/adresse")
@login_required
def recherche_photo_adresse():
    recherche = request.args.get("q", None)
    page = request.args.get("p", 1)
    results_per_page = request.args.get("n", 10)

    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1

    if isinstance(results_per_page, str) and results_per_page.isdigit():
        results_per_page = int(results_per_page)
    else:
        results_per_page = 10

    # scission de la recherche en plusieurs termes
    # de préférence, la synatxe de la recherche est N_rue rue Code_postal? Ville?
    adresse = extract_adresse(recherche)
    regex_rue = '( ?PARIS ?|(AVENUE|IMPASSE|QUAI|VOIE|RUELLE|BOULEVARD|RUE)( D(E(S?| LA)|U))? )'
    N_rue = adresse.number.number
    Rue = re.sub(regex_rue, '', adresse.road.name.upper())
    Code_postal = adresse.locality.zip
    Code_postal_dpt = re.sub('[0-9]{3}$', '', str(Code_postal))
    if "PARIS" in Rue or re.match('^75[0-9]{3}', str(Code_postal)):
        Arrondissement = re.sub('^0+', '', Code_postal.replace('75', ''))
    else:
        Arrondissement = -1

    if recherche and N_rue != -1:
        query = Classe_db.query.filter(and_(
            Classe_db.Rue.like("%{}%".format(Rue)), Classe_db.N_rue.like(N_rue))
        )
    elif recherche and N_rue != -1 and Arrondissement != -1:
        query = Classe_db.query.filter(and_(
            Classe_db.Rue.like("%{}%".format(Rue)), Classe_db.N_rue.like(N_rue), Classe_db.Arrondissement.like(Arrondissement))
        )
    elif recherche and N_rue == -1:
        query = Classe_db.query.filter(
            Classe_db.Rue.like("%{}%".format(Rue))
        )
    elif recherche and N_rue == -1 and Arrondissement != -1:
        query = Classe_db.query.filter(and_(
            Classe_db.Rue.like("%{}%".format(Rue)), Classe_db.Arrondissement.like(Arrondissement))
        )
    elif recherche and Arrondissement != -1:
        query = Classe_db.query.filter(Classe_db.Arrondissement.like(Arrondissement)
        )
    else:
        query = Classe_db.query

    try:
        resultats = query.paginate(page=page, per_page=results_per_page)
    except Exception:
        return Json_404()

    dict_resultats = {
        "links": {
            "self": request.url
        },
        "data": [
            {str(photo.N_inventaire) : photo.to_json()}
            for photo in resultats.items
        ],
        "meta": {
            "copyright": "2020 - Association Paris Historique",
            "total results": resultats.total
        }
    }

    if resultats.has_next:
        arguments = {
            "p": resultats.next_num,
            "n" : results_per_page
        }
        if recherche:
            arguments["q"] = recherche
        dict_resultats["links"]["next"] = url_for("recherche_photo_adresse", _external=True)+"?"+urlencode(arguments)

    if resultats.has_prev:
        arguments = {
            "p": resultats.prev_num,
            "n": results_per_page
        }
        if recherche:
            arguments["q"] = recherche
        dict_resultats["links"]["prev"] = url_for("recherche_photo_adresse", _external=True)+"?"+urlencode(arguments)

    response = jsonify(dict_resultats)
    return response


@app.route(CHEMIN_API + "/photographie/mot_cle")
@login_required
def recherche_photo_mot_cle():
    recherche = request.args.get("q", None)
    page = request.args.get("p", 1)
    results_per_page = request.args.get("n", 10)

    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1

    if isinstance(results_per_page, str) and results_per_page.isdigit():
        results_per_page = int(results_per_page)
    else:
        results_per_page = 10

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

    dict_resultats = {
        "links": {
            "self": request.url
        },
        "data": [
            {str(photo.N_inventaire): photo.to_json()}
            for photo in resultats.items
        ],
        "meta": {
            "copyright": "2020 - Association Paris Historique",
            "total results": resultats.total
        }
    }

    if resultats.has_next:
        arguments = {
            "p": resultats.next_num,
            "n": results_per_page
        }
        if recherche:
            arguments["q"] = recherche
        dict_resultats["links"]["next"] = url_for("recherche_photo_mot_cle", _external=True) + "?" + urlencode(
            arguments)

    if resultats.has_prev:
        arguments = {
            "p": resultats.prev_num,
            "n": results_per_page
        }
        if recherche:
            arguments["q"] = recherche
        dict_resultats["links"]["prev"] = url_for("recherche_photo_mot_cle", _external=True) + "?" + urlencode(
            arguments)

    response = jsonify(dict_resultats)
    return response
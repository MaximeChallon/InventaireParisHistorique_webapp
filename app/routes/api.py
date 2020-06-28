from ..app import app
from flask import render_template, request, url_for, jsonify
from urllib.parse import urlencode
from flask_login import login_required
from..models.donnees import Classe_db
from ..constantes import CHEMIN_API
import re
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
    # retournement de l'adresse donnée en requête pour la mettre sous la forme Numéro_rue Rue Code_postal Ville
    # si le code postal est au début
    if re.match("^[0-9]{5}[a-zA-Z éèàùêôî-]{0,}[0-9]{0,4}.*$", requete):
        pattern = "^([0-9]{5}[a-zA-Z éèàùêôî-]{0,})([0-9]{0,4}.*)$"
        requete = re.match(pattern, requete).group(2) + re.match(pattern, requete).group(1)
    # si le code postal est en deuxième partie
    elif re.match("^[0-9]{0,4}.*[0-9]{5}[a-zA-Z éèàùêôî-]{0,}$", requete):
        requete=requete
    else:
        requete = requete

    # à partir de l'adresse normalisée, extraction des différents blocs d'information
    if re.match("^[0-9]{0,4}.*[0-9]{5}[a-zA-Z éèàùêôî-]{0,}$", requete):
        bloc_rue = re.sub("[0-9]{5}.*", "", requete)
        bloc_ville = re.match("^[0-9]{0,4}.*([0-9]{5}[a-zA-Z éèàùêôî-]{0,})$", requete).group(1)
    elif re.match("^[0-9]{0,4}.*$", requete):
        bloc_rue = re.sub("[0-9]{5}.*", "", requete)
        bloc_ville = None
    return (bloc_rue, bloc_ville)


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
    try:
        recherche = request.args.get("q", None)
        query = Classe_db.query.get(recherche)
        dict_json = {"data": {str(query.N_inventaire): query.to_json()}
        }
        return jsonify(dict_json)
    except:
        return Json_404()


@app.route(CHEMIN_API + "/photographie/numeros_inventaire")
def multiple_photo_id():
    """
    Permet d'obtenir les données des photograohies comprises dans l'intervalle donné en requête (le séparateur peut être tout sauf un chiffre)
    :return: JSON
    """
    recherche = request.args.get("q", None)
    _from = int(re.sub("[^0-9]+[0-9]+$", "", recherche))
    _to = int(re.sub("[0-9]+[^0-9]+", "", recherche))
    liste_results = []
    while _from <= _to:
        query = Classe_db.query.get(_from)
        # ne retourner que les numéros d'inventaire qui ont des métadonnées; s'il est absent, il n'est pas retourné
        if query != None:
            liste_results.append(query)
        _from += 1
    #structuration des données de sortie
    dict_results = {
            "data": [
                {str(photo.N_inventaire): photo.to_json()}
                for photo in liste_results
            ],
            "meta": {
                "copyright": "2020 - Association Paris Historique",
                "total results": len(liste_results)
            }
        }
    return jsonify(dict_results)


@app.route(CHEMIN_API+"/photographie/adresse")
def recherche_photo_adresse():
    """
    Recherche de photographie par adresse
    :return: JSON
    """
    # récupération des données de l'URL
    recherche = request.args.get("q", None)
    page = request.args.get("p", 1)
    results_per_page = request.args.get("n", 10)

    # gestion de la pagination et du noimbre de résultats par page
    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1

    if isinstance(results_per_page, str) and results_per_page.isdigit():
        results_per_page = int(results_per_page)
    else:
        results_per_page = 10

    # scission de la recherche en plusieurs termes
    # de préférence, la syntaxe de la recherche est N_rue rue Code_postal? Ville?
    bloc_rue, bloc_ville = extract_adresse(recherche)
    regex_rue = '( ?PARIS ?|(AVENUE|IMPASSE|QUAI|VOIE|RUELLE|PLACE|BOULEVARD|RUE)( D(E(S?| LA)|U))? )'
    # traitement du bloc de la rue
    if re.match("([0-9]+)", bloc_rue):
        N_rue = str(re.match("([0-9]+)", bloc_rue).group(1))
    else:
        N_rue = str(-1)
    Rue = re.sub(regex_rue, "", re.sub("[0-9]+ ?","", bloc_rue.upper()))

    # traitement du bloc de la ville
    if re.match("[0-9]{5}", str(bloc_ville)):
        Code_postal = re.match("([0-9]{5})", bloc_ville).group(1)
        Code_postal_dpt = re.sub('[0-9]{3}$', '', str(Code_postal))
        Ville = re.sub("[0-9]{5} ?", "", bloc_ville)
        if "PARIS" in Rue or re.match('^75[0-9]{3}', str(Code_postal)):
            Arrondissement = int(re.sub("^0+", "", Code_postal.replace('75', '')))
        else:
            Arrondissement = -1
    else:
        Code_postal = -1
        Code_postal_dpt = -1
        Ville = ""
        Arrondissement = -1

    # requêtes SQL via SQLAlchemy en fonction des données disponibles récupérées dans l'URL
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

    # initialisation du dictionnaire de retour des résultats
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

    # remplissage des clés de pagination du dictionnaire
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
def recherche_photo_mot_cle():
    """
    Recherche de photographie par mot clé
    :return: JSON
    """
    # récupération des données transmises dans l'URL
    recherche = request.args.get("q", None)
    page = request.args.get("p", 1)
    results_per_page = request.args.get("n", 10)

    # gestion de la pagination et du nombre de résultats par page
    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1

    if isinstance(results_per_page, str) and results_per_page.isdigit():
        results_per_page = int(results_per_page)
    else:
        results_per_page = 10

    mot_cle = recherche.upper()

    # requête dans la base de donéees avec un OR_
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

    # gestion de la pagination des résultats
    try:
        resultats = query.paginate(page=page, per_page=results_per_page)
    except Exception:
        return Json_404()

    # dictionnaire d'accueil des résultats
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

    # remplissage de la clé de pagination dans le dictionnaire
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
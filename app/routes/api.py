from ..app import app, db
from flask import render_template, request, url_for, jsonify
from urllib.parse import urlencode
from..models.donnees import Classe_db
from ..constantes import CHEMIN_API


def Json_404():
    response = jsonify({"erreur": "Requête impossible"})
    response.status_code = 404
    return response


@app.route(CHEMIN_API + "/photographie/<photo_id>")
def single_photo_id(photo_id):
    try:
        query = Classe_db.query.get(photo_id)
        dict_json = {"data": {str(query.N_inventaire) : query.to_json()}
        }
        return jsonify(dict_json)
    except:
        return Json_404()
from flask import request, url_for
from urllib.parse import urlencode

class Classe_API():
    @staticmethod
    def return_json(recherche, resultats, results_per_page):
        # initialisation du dictionnaire de retour des résultats
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

        # remplissage des clés de pagination du dictionnaire
        if resultats.has_next:
            arguments = {
                "p": resultats.next_num,
                "n": results_per_page
            }
            if recherche:
                arguments["q"] = recherche
            dict_resultats["links"]["next"] = url_for("recherche_photo_adresse", _external=True) + "?" + urlencode(
                arguments)

        if resultats.has_prev:
            arguments = {
                "p": resultats.prev_num,
                "n": results_per_page
            }
            if recherche:
                arguments["q"] = recherche
            dict_resultats["links"]["prev"] = url_for("recherche_photo_adresse", _external=True) + "?" + urlencode(
                arguments)
        return dict_resultats

    @staticmethod
    def check_n_p(page, results_per_page):
        # gestion de la pagination et du nombre de résultats par page
        if isinstance(page, str) and page.isdigit():
            page = int(page)
        else:
            page = 1

        if isinstance(results_per_page, str) and results_per_page.isdigit():
            results_per_page = int(results_per_page)
        else:
            results_per_page = 10

        return page, results_per_page
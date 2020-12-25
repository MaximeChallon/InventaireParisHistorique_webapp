from ..app import db

def extract_filters(form):
    dico_filters = {}
    if form.Rue.data != "":
        dico_filters["Rue"] = form.Rue.data
    if form.Arrondissement.data != "":
        dico_filters["Arrondissement"] = form.Arrondissement.data
    print(dico_filters)
    return dico_filters

def where_clause(filters):
    where_clause = ""
    for entree in filters:
        if type(filters[entree]) == str:
            if len(where_clause) == 0:
                where_clause = " where " + entree + " like '%" + filters[entree].upper()+ "%'"
            else:
                where_clause = where_clause + " and " + entree + " like '%" + filters[entree].upper() + "%'"
        if type(filters[entree]) == list:
            if len(where_clause) == 0:
                where_clause = " where " + entree + " in " + str(filters[entree]).replace("[", "(").replace("]", ")")
            else:
                where_clause = where_clause +  " and " + entree + " in " + str(filters[entree]).replace("[", "(").replace("]", ")")
    return where_clause

def search(form):
    filters = extract_filters(form)
    if filters:
        where = where_clause(filters)
        resultats = db.session.execute("""select * from Classe_db """ + where + """ limit 2 offset 0""").fetchall()
        print(where)
        print(resultats)
    print(filters)
    return "ok"
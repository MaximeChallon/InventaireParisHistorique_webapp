from ..app import db

def extract_filters(form):
    dico_filters = {}
    if form.Rue.data != "":
        dico_filters["Rue"] = form.Rue.data
    if form.Arrondissement.data != "":
        dico_filters["Arrondissement"] = form.Arrondissement.data
    if form.Mots_cles.data != "":
        dico_filters["Mot_cle"] = form.Mots_cles.data
    if form.Support.data != "":
        dico_filters["Support"] = form.Support.data
    if form.Taille.data != "":
        dico_filters["Taille"] = form.Taille.data
    if form.Photographe.data != "":
        dico_filters["Photographe"] = form.Photographe.data
    return dico_filters

def where_clause(filters):
    where_clause = ""
    for entree in filters:
        #filtre des champs texte libres
        if type(filters[entree]) == str:
            if len(where_clause) == 0:
                where_clause = " where " + entree + " like '%" + filters[entree].upper()+ "%'"
            else:
                where_clause = where_clause + " and " + entree + " like '%" + filters[entree].upper() + "%'"
        # filtres de liste sauf pour mot-clé
        if type(filters[entree]) == list and entree != "Mot_cle" and filters[entree]:
            if len(where_clause) == 0:
                where_clause = " where " + entree + " in " + str(filters[entree]).replace("[", "(").replace("]", ")")
            else:
                where_clause = where_clause +  " and " + entree + " in " + str(filters[entree]).replace("[", "(").replace("]", ")")
        # filtre du mot-clé
        if type(filters[entree]) == list and entree == "Mot_cle" and filters[entree]:
            if len(where_clause) == 0:
                where_clause = " where (" + entree + "1" + " in " + str(filters[entree]).replace("[", "(").replace("]", ")") + " or " +\
                                entree + "2" + " in " + str(filters[entree]).replace("[", "(").replace("]", ")") + " or " +\
                                entree + "3" + " in " + str(filters[entree]).replace("[", "(").replace("]", ")") + " or " +\
                                entree + "4" + " in " + str(filters[entree]).replace("[", "(").replace("]", ")") + " or " +\
                                entree + "5" + " in " + str(filters[entree]).replace("[", "(").replace("]", ")") + " or " +\
                                entree + "6" + " in " + str(filters[entree]).replace("[", "(").replace("]", ")") + ")"
            else:
                where_clause = where_clause +  " and " + "(" + entree + "1" + " in " + str(filters[entree]).replace("[", "(").replace("]", ")") + " or " +\
                                entree + "2" + " in " + str(filters[entree]).replace("[", "(").replace("]", ")") + " or " +\
                                entree + "3" + " in " + str(filters[entree]).replace("[", "(").replace("]", ")") + " or " +\
                                entree + "4" + " in " + str(filters[entree]).replace("[", "(").replace("]", ")") + " or " +\
                                entree + "5" + " in " + str(filters[entree]).replace("[", "(").replace("]", ")") + " or " +\
                                entree + "6" + " in " + str(filters[entree]).replace("[", "(").replace("]", ")") + ")"   
    return where_clause

def search(form, limit):
    filters = extract_filters(form)
    if filters:
        where = where_clause(filters)
        resultats = db.session.execute("""select * from Classe_db """ + where + """ limit """ + str(limit)+ """ offset 0""").fetchall()
        print(where)
        print(resultats)
    print(filters)
    return "ok"
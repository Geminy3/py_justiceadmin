from enum import Enum

URL_BUILDER = {
    'juridiction' : 'model_noTyped/openData/{juridiction}/null/{nb_recherche}',
    'type' : 'model_noTyped/openData/null/{type}/{nb_recherche}',
    'date' : 'model_Dates/openData/Date_Lecture/{date_start}/{date_end}/{nb_recherche}',
    'keywords' : 'Simple_Search/openData/{keywords}/{nb_recherche}',
    'keywordsdate' : 'model_searchANDdates/openData/Date_Lecture/{keywords}/{date_start}/{date_end}/{nb_recherche}',
    'keywordstype' : 'Check_Search/openData/{type}/{keywords}/{nb_recherche}',
    'keywordsjuridiction' : 'model_search_juri/openData/{juridiction}/{keywords}/{nb_recherche}',
    'typejuridiction' : 'model_noTyped/openData/{juridiction}/{type}/{nb_recherche}',
    'datejuridiction' : 'model_date_juri/openData/Date_Lecture/{juridiction}/{date_start}/{date_end}/{nb_recherche}',
    'datetype' : 'Date_Checkbox/openData/Date_Lecture/{type}/{date_start}/{date_end}/null/{nb_recherche}',
    'keywordsdatetype' : 'model_all/openData/Date_Lecture/{keywords}/{type}/{date_start}/{date_end}/{nb_recherche}',
    'keywordsdatejuridiction' : 'model_search_date_juri/openData/Date_Lecture/{keywords}/{juridiction}/{date_start}/{date_end}/{nb_recherche}',
    'keywordstypejuridiction' : 'model_search_check_juri/openData/{type}/{juridiction}/{keywords}/{nb_recherche}',
    'datetypejuridiction' : 'Date_Checkbox/openData/Date_Lecture/{type}/{juridiction}/{date_start}/{date_end}/{nb_recherche}',
    'all' : 'model_ABCD/openData/Date_Lecture/{keywords}/{type}/{juridiction}/{date_start}/{date_end}/{nb_recherche}',
    'get_dec' : 'testView/openData/unHighlight/{id_xml}/{juridiction}/{id_dec}'
}

class type_dec(Enum):
    decision = "Décision"
    ordonnance = "Ordonnance"

class dec_online(Enum):
    en_ligne = 'lastModified'
    rendue = 'Date_Lecture'

class juridiction(Enum):
    ta = "TA"
    ca = "CAA"
    ce = "CE"

class locationCA(Enum):
    bordeaux = "33"
    douai = "59"
    lyon = "69"
    marseille = "13"
    nancy = "54"
    nantes = "44"
    paris = "75"
    toulouse = "31"
    versailles = "78"

class locationTA(Enum):
    bordeaux = "33"
    douai = "59"
    lyon = "69"
    marseille = "13"
    nancy = "54"
    nantes = "44"
    paris = "75"
    toulouse = "31"
    versailles = "78"
    amiens = "80"
    nice = "06"
    reunion = "101"
    martinique = "102"
    polynesiefrancaise = "103"
    nouvellecaledonie = "104"
    guadeloupe = "105"
    guyanne = "106"
    saintmartin = "108"
    saintbarthelemy = "109"
    caen = "14"
    bastia = "20"
    dijon = "21"
    besancon = "25"
    nimes = "30"
    montpellier = "34"
    rennes = "35"
    grenoble = "38"
    orleans = "45"
    chalonenchampagne = "51"
    lille = "59"
    clermontferrand = "63"
    pau = "64"
    strasbourg = "67"
    mayotte = "107"
    rouen = "76"
    melun = "77"
    toulon = "83"
    poitiers = "86"
    limoges = "87"
    montreuil = "93"
    cergypontoise = "95"

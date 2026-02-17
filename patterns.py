pattern_get_text = "testView/openData/blabla/DTA_2402627_20241213/TA21/2402627"

list_all_url_pattern = [
    
    # 1 argument
    ## TEXT
    "Simple_Search/openData/{params_strings}/{nb_recherche}",
    ## Juridicition
    "model_noTyped/openData/{params_jurisdiction}/null/{nb_recherche}",
    ## type d'acte
    "model_noTyped/openData/null/{params_decision_or_ordonnance}/{nb_recherche}",
    ## DATE
    "model_Dates/openData/Date_Lecture/{params_date_start}/{params_date_end}/{nb_recherche}",

    # 2 arguments
    ## TEXT & Type d'acte
    "Check_Search/openData/{params_decision_or_ordonnance}/{params_strings}/{nb_recherche}",
    ## TEXT & Juridiction
    "model_search_juri/openData/{params_jurisdiction}/{params_strings}/{nb_recherche}",
    ## TEXT & DATE
    "model_searchANDdates/openData/Date_Lecture/{params_strings}/{params_date_start}/{params_date_end}/{nb_recherche}",
    ## Juridiction & DATE
    "model_date_juri/openData/Date_Lecture/{params_jurisdiction}/{params_date_start}/{params_date_end}/{nb_recherche}",
    ## Juridiction & Type d'acte
    "model_noTyped/openData/{params_jurisdiction}/{params_decision_or_ordonnance}/{nb_recherche}",
    ## Type d'acte & DATE
    "Date_Checkbox/openData/Date_Lecture/{params_decision_or_ordonnance}/{params_date_start}/{params_date_end}/null/{nb_recherche}",


    # 3 arguments
    ## Type d'acte & Juridiction & DATE
    "Date_Checkbox/openData/Date_Lecture/{params_decision_or_ordonnance}/{params_jurisdiction}/{params_date_start}/{params_date_end}/{nb_recherche}",
    ## Type d'acte & Juridiction & TEXT
    "model_search_check_juri/openData/{params_decision_or_ordonnance}/{params_jurisdiction}/{params_strings}/{nb_recherche}",
    ## Type d'acte & DATE & TEXT
    "model_all/openData/Date_Lecture/{params_strings}/{params_decision_or_ordonnance}/{params_date_start}/{params_date_end}/{nb_recherche}",
    ## DATE & TEXT & Juridiction
    "model_search_date_juri/openData/Date_Lecture/{params_strings}/{params_jurisdiction}/{params_date_start}/{params_date_end}/{nb_recherche}",
    
    
    # Tous les arguments
    "model_ABCD/openData/Date_Lecture/{params_strings}/{params_decision_or_ordonnance}/{params_jurisdiction}/{params_date_start}/{params_date_end}/{nb_recherche}"
]
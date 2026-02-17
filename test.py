from py_justiceadmin import JA_requester

if __name__ == "__main__":
    client = JA_requester(
        base_url='https://opendata.justice-administrative.fr/recherche/api/', 
    )

    # To access parameters for juridiction and ville
    #client.get_parameters()

    query = {
        'keywords' : '"trouble anormal de voisinage"', 
        'date_start' : '2021-01-20',
        'date_end' : '2026-01-01',
        'type' : "Ordonnance",
        'juridiction' : "ta", #ta, ca, ce
        'ville' : ["bordeaux", "paris"], 
        'OnLine' : True, #True / False #Pas encore vraiment implémenté
        'nb_recherche' : 10000
    }


    response = client.get_query(params = query)
    print(response)
    # for dec in client.data['hits']:
    #     print(dec)

    # To get a specific dec from reponses
    client.get_decision(response = client.data['hits'][1])
    #print(client.get_decision(response = client.data['hits'][1]))
    

    # To get all the decision from a respones
    decisions = client.get_all_decisions()
    #print(decisions)

    # To get all the parameters for `juridiction` and `ville`
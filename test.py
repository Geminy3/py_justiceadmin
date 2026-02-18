from py_justiceadmin import JA_requester

if __name__ == "__main__":
    client = JA_requester(
        base_url='https://opendata.justice-administrative.fr/recherche/api/', 
        query_verbose=False
    )

    # To access parameters for juridiction and ville
    # client.get_parameters()

    response = client.get_query(
        keywords = "trouble anormal de voisinage", 
        exact_sentence=True,
        date_start = '2021-01-20',
        date_end = '2026-01-01',
        type = "Ordonnance",
        juridiction = "ta",
        ville = ["bordeaux", "paris"], 
        OnLine = True,
        nb_recherche = 10000,
        timeout = 30
    )
    print(response)
    # for dec in client.data['hits']:
    #     print(dec)

    # To get a specific dec from reponses
    client.get_decision(response = client.data['hits'][1])
    # print(client.dec)
    print(client.dec)
    #print(client.get_decision(response = client.data['hits'][1]))
    

    # To get all the decision from a respones
    # decisions = client.get_all_decisions()
    # print(decisions)

    # To get all the parameters for `juridiction` and `ville`
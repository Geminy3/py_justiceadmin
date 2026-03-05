from py_justiceadmin import JA_requester

if __name__ == "__main__":
    client = JA_requester(
        base_url='https://opendata.justice-administrative.fr/recherche/api/', 
        query_verbose=False
    )

    # To access parameters for juridiction and ville
    # client.get_parameters()

    response = client.get_query(
        keywords = '"article L.2212-2 du code général des collectivités territoriales"|"article L2212-2 du code général des collectivités territoriales"', 
        exact_sentence=False,
        date_start = None,#'2021-01-20',
        date_end = None,#'2026-01-01',
        type = None,#"Ordonnance",
        juridiction = None,#"ta",
        ville = None,#["bordeaux", "paris"], 
        OnLine = True,
        nb_recherche = 10000,
        timeout = 30
    )
    print("RESPONSE : ", response)
    # for i, dec in enumerate(client.data):
    #     print(f'{i} - {dec}')

    # To get a specific dec from reponses
    # client.get_decision(response = client.data[1])
    # print(client.dec)
    # print(client.get_decision(response = client.data[1]))
    

    # To get all the decision from a response
    decisions = client.get_all_decisions(client.data), #There is a verbose option to see progress
    print(decisions)

    # If you want to get all the decision from another data object
    #  The data should look like data = [{"id" : "id", "_source" : {...}}]
    # decisions = client.get_all_decisions(data)

    # To get all the parameters for `juridiction` and `ville`
from py_justiceadmin.api import JA_requester

if __name__ == "__main__":
    client = JA_requester(
        base_url='https://opendata.justice-administrative.fr/recherche/api/', 
    )

    # To access parameters for juridiction and ville
    #client.get_parameters()

    query = {
        'keywords' : '"trouble anormal de voisinage"', 
        'date_start' : None,#'2021-01-20',
        'date_end' : None, #'2023-01-01',
        'type' : None,#"Ordonnance",
        'juridiction' : 'ta', #ta, ca, ce
        'ville' : ["bordeaux", "paris"], 
        'OnLine' : True, #True / False #Pas encore vraiment implémenté
        'nb_recherche' : 10000
    }



    response = client._query(params = query)
    print(len(client.data['hits']))
    #print(client.data['hits'][0])
    # for dec in client.data['hits']:
    #     print(dec)

    # To get a specific dec from reponses
    client.get_dec(client.data['hits'][2])
    #print(client.dec)
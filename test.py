from py_justiceadmin import JA_requester

if __name__ == "__main__":
    client = JA_requester(
        base_url='https://opendata.justice-administrative.fr/recherche/api/', 
    )

    response = client._query(
            params={
                'keywords' : '"trouble anormal de voisinage"', 
                'date_start' : None,#'2021-01-20',
                'date_end' : None, #'2023-01-01',
                'type' : None,#"Ordonnance",
                'juridiction' : None,
                'ville' : None, 
                'OnLine' : None, #True / False
                'nb_recherche' : 10000
                }
        )
    print(len(client.data['hits']))
    #print(client.data['hits'][0])
    # for dec in client.data['hits']:
    #     print(dec)
    client.get_dec(client.data['hits'][2])
    #print(client.dec)
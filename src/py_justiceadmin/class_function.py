from .classes import (
    Juridiction,
    Type_dec,
    Date,
    Keywords,
    Nb_recherche, 
)

def define_dec_from_res(
            response: dict = None,
    ) -> dict:
        
        response = response['_source']
        id_xml = response["Identification"].replace(".xml", "")
        date = response["Date_Lecture"]
        id_dec = response['Numero_Dossier']
        jurisdiction = response["Code_Juridiction"]
        return {
            'id_xml' : id_xml, 
            'date' : date,
            'id_dec' : id_dec, 
            'juridiction' : jurisdiction
        }

def convert_query_params(
            params: dict = {}
    ):
        for k, v in params.items():
            match k:
                case 'nb_recherche':
                    nb_recherche = Nb_recherche(params[k])
                    params[k] = nb_recherche.nb_recherche
                case "juridiction":
                    juridiction = Juridiction(params['ville'], v)
                    params[k] = juridiction._query_args()
                case "type":
                    type_dec = Type_dec(v)
                    params[k] = type_dec._query_args()
                case "date_start":
                    date = Date(v, params["date_end"])
                    date_start, date_end = date._query_args()
                case "keywords":
                    keywords = Keywords(v)
                    params[k] = keywords._query_args()
        if 'date_start' in params or 'date_end' in params:
            params['date'] = {
                            'date_start' : date_start, 
                            'date_end' : date_end
                        }
            params.pop('date_start')
            params.pop('date_end')
        params["ville"] = None
        return params
from py_justiceadmin.exceptions import (
    JAParamsMissingError
)
from .class_function import define_dec_from_res, convert_query_params

class Query():

    def __init__(
            self, 
            params: dict = {}, 
            list_args = None
    ) -> None:

        params = convert_query_params(params)   
        self.params = {
            key: value for key, value in params.items() if value is not None
        }
        #print(self.params)
        self.nb_recherche = params['nb_recherche'] if 'nb_recherche' in params else 10000
        self.list_args = ['juridiction', 'date', 'type', 'keywords'] if list_args is None else list_args
        
    def _build_url(self) -> str:
        
        used_params = [key for key in self.params if key in self.list_args]
        match len(used_params):
            case 0:
                raise JAParamsMissingError("No arguments provided to the API")
            case 1:
                if 'juridiction' in used_params:
                    self.base_url = f'model_noTyped/openData/{self.params['juridiction']}/null/{self.nb_recherche}'
                elif 'type' in used_params:
                    base_url = f'model_noTyped/openData/null/{self.params['type']}/{self.nb_recherche}'
                elif 'date' in used_params:
                    base_url = f'model_Dates/openData/Date_Lecture/{self.params['date']['date_start']}/{self.params['date']['date_end']}/{self.nb_recherche}',
                elif 'keywords' in used_params:
                    base_url = f'Simple_Search/openData/{self.params['keywords']}/{self.nb_recherche}'
            case 2:
                if 'juridiction' in used_params:
                    if 'type' in used_params:
                        base_url = f'model_noTyped/openData/{self.params['juridiction']}/{self.params['type']}/{self.nb_recherche}'
                    elif 'date' in used_params:
                        base_url = f'model_date_juri/openData/Date_Lecture/{self.params['juridiction']}/{self.params['date']['date_start']}/{self.params['date']['date_end']}/{self.nb_recherche}'
                    elif 'keywords' in used_params:
                        base_url = f'model_search_juri/openData/{self.params['juridiction']}/{self.params['keywords']}/{self.nb_recherche}'
                elif 'type' in used_params:
                    if 'date' in used_params:
                        base_url = f'Date_Checkbox/openData/Date_Lecture/{self.params['type']}/{self.params['date']['date_start']}/{self.params['date']['date_end']}/null/{self.nb_recherche}'
                    elif 'keywords' in used_params:
                        base_url = f'Check_Search/openData/{self.params['type']}/{self.params['keywords']}/{self.nb_recherche}'
                elif 'date' in used_params and 'keywords' in used_params:
                    base_url = f'model_searchANDdates/openData/Date_Lecture/{self.params['keywords']}/{self.params['date']['date_start']}/{self.params['date']['date_end']}/{self.nb_recherche}'
            case 3:
                if 'juridiction' in used_params and 'type' in used_params and 'date' in used_params:
                    base_url = f'Date_Checkbox/openData/Date_Lecture/{self.params['type']}/{self.params['juridiction']}/{self.params['date']['date_start']}/{self.params['date']['date_end']}/{self.nb_recherche}'
                elif 'juridiction' in used_params and 'type' in used_params and 'keywords' in used_params:
                    base_url = f'model_search_check_juri/openData/{self.params['type']}/{self.params['juridiction']}/{self.params['keywords']}/{self.nb_recherche}'
                elif 'juridiction' in used_params and 'date' in used_params and 'keywords' in used_params:
                    base_url = f'model_search_date_juri/openData/Date_Lecture/{self.params['keywords']}/{self.params['juridiction']}/{self.params['date']['date_start']}/{self.params['date']['date_end']}/{self.nb_recherche}'
                elif 'type' in used_params and 'date' in used_params and 'keywords' in used_params:
                    base_url = f'model_all/openData/Date_Lecture/{self.params['keywords']}/{self.params['type']}/{self.params['date']['date_start']}/{self.params['date']['date_end']}/{self.nb_recherche}'
            case 4:
                base_url = f'model_ABCD/openData/Date_Lecture/{self.params['keywords']}/{self.params['type']}/{self.params['juridiction']}/{self.params['date']['date_start']}/{self.params['date']['date_end']}/{self.nb_recherche}'
        self.url_query = base_url
        #print(self.url)
        return self.url_query
    
class Decision():

    def __init__(
            self,
            response: dict = {}
    ):
        self.decision = define_dec_from_res(response)
        self.params = {
            key: value for key, value in self.decision.items() if value is not None
        }
    
    def _build_url(self) -> str:
        
        used_params = [key for key in self.params]
        if 'id_xml' in used_params and 'id_dec' in used_params and 'juridiction' in used_params:
            self.url_dec = f'testView/openData/unHighlight/{self.params['id_xml']}/{self.params['juridiction']}/{self.params['id_dec']}'
        else:
            raise JAParamsMissingError(f"Missing argument to fetch decision")
        #print(self.url)
        return self.url_dec

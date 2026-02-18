from unidecode import unidecode
import re
from datetime import datetime
from py_justiceadmin.exceptions import (
    JAParamsValueError,
)
from py_justiceadmin.enums import (
    juridiction,
    locationCA,
    locationTA,
    type_dec,
    dec_online
)

def convert_text(
        text:str = ''
):
    """
    Converts the input text to a standardized format by:
    1. Converting to lowercase
    2. Removing diacritics using unidecode
    3. Removing hyphens
    4. Removing spaces

    Args:
        text (str): The input text to be converted

    Returns:
        str: The converted text in lowercase, without diacritics, hyphens, or spaces
    """
    text = text.lower()
    text = unidecode(text)
    text = re.sub(pattern="-", repl="", string=text)
    text = text.replace(" ", "")
    return text


class Juridiction():

    def __init__(self, ville, juridictions):

        if isinstance(ville, list):
            self.ville = [convert_text(v) for v in ville]
        elif isinstance(ville, str):
            self.ville = convert_text(ville)
        elif ville == None:
            self.ville = None
        else:
            raise JAParamsValueError("Wrong city argument")

        if isinstance(juridictions, list):
            self.juridictions = [convert_text(j) for j in juridictions if j in juridiction._member_names_]
            self.juris = self._create_juridiction()
        elif isinstance(juridictions, str) and juridictions in juridiction._member_names_:
            self.juridictions = convert_text(juridictions)
            self.juris = self._create_juridiction()
        elif juridictions == None:
            self.juridictions = None
            self.juris = self._create_juridiction()
        else:
            raise JAParamsValueError("Wrong juridiction argument")
        

    def _create_juridiction(self):
        juris = []
        if isinstance(self.juridictions, list):
            for j in self.juridictions:
                juris.extend(self._process_ville(j))
        elif isinstance(self.juridictions, str):
            juris.append(self._process_ville(self.juridictions))
            if len(juris) == 1:
                juris = juris[0]
        elif self.juridictions == None:
            return None
        return juris

    def _process_ville(self, j):
        
        if isinstance(self.ville, str) or j == juridiction.ce.name:
            return [self._check_city(self.ville, j)]
        elif isinstance(self.ville, list):
            return [self._check_city(v, j) for v in self.ville if self._check_city(v, j) != None]
        elif self.ville == None:
            return [self._check_city(v, j) for v in locationTA._member_names_ if self._check_city(v, j) != None]

    def _check_city(self, v, j):
        if j == juridiction.ca.name:
            if v in locationCA._member_names_:
                res = (juridiction[j], locationCA[v])
            else:
                res = None
        elif j == juridiction.ta.name:
            if v in locationTA._member_names_:
                res = (juridiction[j], locationTA[v])
            else:
                res = None
        elif j == juridiction.ce.name:
            res = (juridiction[j],None)
        return res
    
    def _query_args(self):
        if self.juris == None:
            return None
        elif len(self.juris) > 1:
            stock = []
            for item in self.juris:
                if item[0] != juridiction.ce:
                    stock.append(item[0].value+item[1].value)
                else:
                    stock.append(item[0].value)
            return(' OR '.join(stock))
        else:
            print(self.juris)
            if self.juris[0][0] != juridiction.ce:
                return ''.join([item[0].value+item[1].value for item in self.juris])
            else:
                return self.juris[0][0].value

class Type_dec():

    def __init__(self, _type):
        if isinstance(_type, str) and convert_text(_type) in type_dec._member_names_:
            self.type = type_dec[convert_text(_type)]
        elif isinstance(_type, list):
            if len(_type) == 2 and [convert_text(name) for name in _type].sort() == ["decision", "ordonnance"]:
                self.type = None
            elif len(_type) == 1:
                return Type_dec(_type[0])
            else:
                raise JAParamsValueError("Wrong type argument")
        else:
            if _type == None:
                self.type = None
            else:
                raise JAParamsValueError("Wrong type argument")

    def _query_args(self):
        if self.type != None:
            return self.type.value
        else:
            return self.type

class Date():
    # Date format is YYYY-MM_DD
    def __init__(self, date_start, date_end):
        if date_start is not None:
            if re.match("^\\d{4}-\\d{2}-\\d{2}$", date_start) is not None:
                self.date_start = datetime.strptime(date_start, "%Y-%m-%d")
            else:
                raise JAParamsValueError("Wrong date_start argument")
        else:
            self.date_start = None
            date_end = None
        if date_end is not None:
            if re.match("^\\d{4}-\\d{2}-\\d{2}$", date_end) is not None:
                self.date_end = datetime.strptime(date_end, "%Y-%m-%d")
                if self.date_end < self.date_start:
                    raise JAParamsValueError("Wrong date argument, date_end before date_start")
            else:
                raise JAParamsValueError("Wrong date_end argument")
        else:
            if self.date_start is not None:
                self.date_end = "false"
            else:
                self.date_end = None

    def _query_args(self):
        if self.date_end == None and self.date_start == None:
            return(self.date_start, self.date_end)
        elif self.date_start != None and self.date_end == "false":
            return(str(self.date_start.date()), self.date_end)
        else:
            return(str(self.date_start.date()), str(self.date_end.date()))

        

        

class Keywords():

    def __init__(self, query_string):
        self.query_string = query_string
        #print(self.query_string)

    def _query_args(self):

        return self.query_string
    
class Dec_online():

    def __init__(self, _dec_online):
        if _dec_online:
            self.dec_online = dec_online.en_ligne
        elif _dec_online == False:
            self.dec_online = dec_online.rendue
        else:
            JAParamsValueError("Wrong Online argument")
    
    def _query_args(self):
        return self.dec_online
    
class Nb_recherche():

    def __init__(self, nb):
        if isinstance(nb, int):
            if nb > 0 and nb <= 10000:
                self.nb_recherche = nb
            else:
                raise JAParamsValueError("Incorrect Number (inf to 0 or sup to 10.000)")
        elif nb == None:
            self.nb_recherche = 200
        else:
            raise JAParamsValueError

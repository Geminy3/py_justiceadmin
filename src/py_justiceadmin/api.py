import logging
import os
import json
import re
from unidecode import unidecode
from urllib import (
    parse,
    request as req,
    error as err
)
from .exceptions import (
    ERROR_CODES_TO_EXCEPTIONS,
    JAParamsValueError,
    JAParamsMissingError
)
from .enums import (
    URL_BUILDER,
    juridiction,
    locationCA,
    locationTA
)

from .classes import (
    _juridiction,
    _type_dec,
    _date,
    _query_string,
    _nb_recherche
)

__version__ = "0.0.1"

class JA_requester():

    def __init__(
            self,
            base_url: str | None = None,
            JA_headers : dict = {},
            http_proxy: str | None = None,
            https_proxy: str | None = None,
            default_timeout: int = 10,
            logging_level: int = logging.ERROR
    ):
        #Build HTTP Client

        JA_base_url = base_url or os.environ['JA_BASE_URL']
        
        self.JA_base_url = JA_base_url
        self.JA_headers = JA_headers
        proxies = {
            **({"http": http_proxy} if http_proxy else {}),
            **({"https": https_proxy} if https_proxy else {}),
        }

        self.proxy_handler = req.ProxyHandler(proxies=proxies)
        self.url_opener = req.build_opener(self.proxy_handler)
        self.default_timeout = default_timeout

        self.__version__ = __version__

        self.client_headers = {
            **JA_headers,
            "User-Agent": f"JA_requester {self.__version__}",
        }

        self._logger = logging.getLogger("JA_requester")
        if len(self._logger.handlers) == 0:
            handler = logging.StreamHandler()
            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            handler.setFormatter(formatter)
            self._logger.addHandler(handler)
        self._logger.setLevel(level=logging_level)

        return None
        
    def get_dec(
            self,
            response: dict = None, 
            timeout: int = 30
    ) -> dict:
        
        res = self._define_dec_from_res(response)
        query = parse.quote_plus(
            self._url_dec(**res)
        )
        url = f"{self.JA_base_url.rstrip("/")}/{query}"
        
        request = req.Request(
            method='GET',
            url=url,
        )
        self.dec = self._build_requests(request, timeout=60)

    def _query(
            self,
            method: str = "GET",
            params: dict = {},
            timeout: int | None = None
    ) -> dict:
        
        params = self._convert_params(params)
        query = parse.quote_plus(
            self._build_url(params)
        )
        url = f"{self.JA_base_url.rstrip("/")}/{query}"
        
        self._logger.info(f"REQUEST METHOD URL: {method} {url}")
        self._logger.info(f"REQUEST PARAMETERS: {query}")
        
        request = req.Request(
            method=method,
            url=url,
        )

        self.data = self._build_requests(request, timeout=timeout)
        return self.data['total']['value']

    def _build_requests(
            self,
            request: req.Request,
            timeout: int = 30

    ) -> dict:
        for key, value in self.client_headers.items():
            request.add_header(key, value)

        try:
            with self.url_opener.open(request, timeout=timeout or self.default_timeout) as response:
                content = response.read()

                self._logger.info(f"RESPONSE STATUS : {response.status}")
                self._logger.info(f"RESPONSE HEADERS: {response.headers}")
                self._logger.debug(f"RESPONSE CONTENT: {content.decode('utf-8')}")

                data = json.loads(content)

        except err.HTTPError as exc:
            if exc.status in ERROR_CODES_TO_EXCEPTIONS:
                exception = ERROR_CODES_TO_EXCEPTIONS[exc.status]
                raise exception from exc
            else:
                raise exc
        except Exception as exc:
            raise exc
        
        return data['decisions']['body']['hits']


    def _define_dec_from_res(
            self,
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
    
    def _url_dec(
            self, 
            **kwargs
    ) -> str:
        
        params = {**kwargs}
        #print(params)
        url = URL_BUILDER["get_dec"]
        for key in params:
            url = url.replace(key, params[key])
        query = url.replace('{', '').replace('}', '')
        return query

    def _build_url(
            self,
            params: dict = {}
    ):
        query = []
        nb_recherche = params.pop("nb_recherche")
        for k, v in params.items():
            if isinstance(v, bool):
                next
            elif v != None and len(v) > 0:
                if k.startswith("date") and "date" not in query:
                    query.append("date")
                elif not k.startswith("date"):
                    query.append(k)
        if len(query) == 0:
            raise JAParamsMissingError("No arguments provided to the API")
        url = URL_BUILDER[''.join(query)]
        for k in query:
            if k == 'date':
                url = re.sub(string=url, pattern=f'{k}_start', repl=params[k+'_start']).replace("{", "").replace("}", "")
                url = re.sub(string=url, pattern=f'{k}_end', repl=params[k+'_end']).replace("{", "").replace("}", "")
            elif k == 'juridiction' and isinstance(params['juridiction'], list):
                pass
            else:
                url = re.sub(string=url, pattern=f'{k}', repl=params[k]).replace("{", "").replace("}", "")
        url = re.sub(string=url, pattern="nb_recherche", repl=str(nb_recherche))
        return url
        
    def _convert_params(
            self,
            params: dict = {}
    ):

        for k, v in params.items():
            match k:
                case 'nb_recherche':
                    self.nb_recherche = _nb_recherche(params[k])
                    params[k] = self.nb_recherche.nb_recherche
                case "juridiction":
                    self.juridiction = _juridiction(params['ville'], v)
                    params[k] = self.juridiction._query_args()
                case "type":
                    self.type_dec = _type_dec(v)
                    params[k] = self.type_dec._query_args()
                case "date_start":
                    self.date = _date(v, params["date_end"])
                    date_start, date_end = self.date._query_args()
                    params[k] = date_start
                    params["date_end"] = date_end
                case "keywords":
                    self.keywords = _query_string(v)
                    params[k] = self.keywords._query_args()
        
        params["ville"] = None
        print(params)
        return params

    def grab_decision_text(
            self,
            id: str | None = None
    ):
        return None
    
    def get_parameters(self):
        self.parameters = {
            'juridiction' : juridiction._member_names_,
            'locationCA' : locationCA._member_names_,
            'locationTA' : locationTA._member_names_
        }
        for param in self.parameters:
            print(f'----- {param.upper()} -----')
            for value in self.parameters[param]:
                print(value)
        return self.parameters
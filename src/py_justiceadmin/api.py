import logging
import re
import json
from urllib import (
    parse,
    request as req,
    error as err
)
from py_justiceadmin.classes.classes_params import Decision, Query
from py_justiceadmin.exceptions import ERROR_CODES_TO_EXCEPTIONS, JAParamsMissingError
from py_justiceadmin.enums import (
    juridiction,
    locationCA,
    locationTA, 
    type_dec, 
    dec_online
)

__version__ = "0.2.5"

class JA_requester():

    def __init__(
            self,
            base_url: str | None = 'https://opendata.justice-administrative.fr/recherche/api/',
            JA_headers : dict = {},
            http_proxy: str | None = None,
            https_proxy: str | None = None,
            default_timeout: int = 10,
            logging_level: int = logging.ERROR, 
            query_verbose: bool = True
    ):
        #Build HTTP Client
        if base_url == None:
            raise JAParamsMissingError("Missing endpoint url to requests the API")
        else:
            self.JA_base_url = base_url
        
        self.JA_headers = JA_headers
        proxies = {
            **({"http": http_proxy} if http_proxy else {}),
            **({"https": https_proxy} if https_proxy else {}),
        }

        self.proxy_handler = req.ProxyHandler(proxies=proxies)
        self.url_opener = req.build_opener(self.proxy_handler)
        self.default_timeout = default_timeout
        self.query_verbose = query_verbose

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
        
    def get_decision(
            self,
            method: str = "GET",
            response: dict = None, 
            timeout: int = 30
    ) -> None:
        
        try:
            if len(self.data) == 0:
                raise JAParamsMissingError("Missing decisions")
            else:
                self.decision = Decision(response)
                self.dec = self._send_requests(
                    query=self.decision,
                    method=method,
                    timeout=timeout
                )
                self.dec['url_show_dec'] = self.decision.url_show_dec
                return self.dec
        except Exception as e:
            raise JAParamsMissingError(f"Missing decision {e}")

    def get_query(
            self,
            method: str = "GET",
            keywords: str | None = '',
            exact_sentence:bool = True,
            date_start: str | None = None,
            date_end: str | None = None,
            type: str | None = None,
            juridiction: str | list | None = None,
            ville: str | list | None = None,
            OnLine: bool | None = None,
            nb_recherche: int = 10000,
            timeout: int | None = None
    ) -> dict:
        
        params = {
            'keywords' : f'"{keywords}"' if exact_sentence else keywords, 
            'date_start' : date_start if isinstance(date_start, str) else None,
            'date_end' : date_end if isinstance(date_end, str) else None,
            'type' : type if isinstance(type, str) else None,
            'juridiction' : juridiction, #ta, ca, ce
            'ville' : ville, 
            'OnLine' : OnLine, #True / False #Pas encore vraiment implémenté
            'nb_recherche' : nb_recherche
        }
        if self.query_verbose:
            print(f"---- QUERY PARAMETERS -----")
            for k, v in params.items():
                print(f"{k} : {v}")
        self.query = Query(params)
        self.response = self._send_requests(
            query=self.query,
            method=method,
            timeout=timeout
        )
        self.data = self.response['hits']
        for i, decision in enumerate(self.data):
            id_dec = re.sub(pattern = "\\.xml.*$", string=decision['_id'], repl="")
            juri_dec = decision['_source']['Code_Juridiction']
            self.data[i]['url_show_dec'] = f'https://opendata.justice-administrative.fr/recherche/shareFile/{juri_dec}/{id_dec}'
        return f"Length reponse : {self.response['total']['value']}"

    def get_all_decisions(
            self,
            verbose: bool = True
    ) -> dict:
        
        try:
            if len(self.data) == 0:
                raise JAParamsMissingError("Missing decisions")
            else:
                all_dec = {}
                for i, dec in enumerate(self.data):
                    if verbose:
                        print(f"{i} - {dec}")
                    all_dec[dec['_id']] = self.get_decision(response = dec)
                return all_dec
        except Exception as e:
            raise JAParamsMissingError(f"Missing decision {e}")

    def _send_requests(
            self,
            method: str = "GET",
            query: Decision|Query = Query(),
            timeout: int = 30
    ) -> dict:
        payload = parse.quote(query._build_url())
        url_query = f"{self.JA_base_url.rstrip("/")}/{payload}"
        if self.query_verbose:
            print(f'URL : {url_query}')
            print("---------------------------")
        self._logger.info(f"REQUEST METHOD URL: {"GET"} {url_query}")
        self._logger.info(f"REQUEST PARAMETERS: {payload}")
        
        request = req.Request(
            method=method,
            url=url_query,
        )

        data = self._build_requests(request, timeout=timeout)
        return data

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
        
    
    def get_parameters(self):
        self.parameters = {
            'juridiction' : juridiction._member_names_,
            'locationCA' : locationCA._member_names_,
            'locationTA' : locationTA._member_names_, 
            'type' : type_dec._member_names_, 
            'OnLine' : dec_online._member_names_
        }
        for k, v in self.parameters.items():
            print(f'----- {k.upper()} -----')
            print(v)
        return self.parameters
from .enums import URL_BUILDER, type_dec, dec_online, juridiction, locationCA, locationTA
from .exceptions import (
    ERROR_CODES_TO_EXCEPTIONS,
    JAParamsValueError,
    JAParamsMissingError, 
)
from .api import JA_requester
from .classes_params import define_dec_from_res, convert_query_params
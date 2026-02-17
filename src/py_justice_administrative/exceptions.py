class JANotFoundError(Exception):
    pass

class JAInvalidRequestError(Exception):
    pass

class JAInvalidCredentialsError(Exception):
    pass

class JAUnauthorizedError(Exception):
    pass

class JASuspiciousActivityError(Exception):
    pass

class JATooManyRequestError(Exception):
    pass

class JAInternalError(Exception):
    pass

class JAParamsValueError(Exception):
    pass

class JAParamsMissingError(Exception):
    pass

ERROR_CODES_TO_EXCEPTIONS = {
    400: JAInvalidRequestError,
    401: JAInvalidCredentialsError,
    403: JAUnauthorizedError,
    404: JANotFoundError,
    423: JASuspiciousActivityError,
    429: JATooManyRequestError,
    500: JAInternalError,
}
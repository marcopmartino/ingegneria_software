import json
import traceback

from requests import HTTPError, RequestException


class HTTPErrorHelper(object):

    @staticmethod
    def extract_message(e: HTTPError) -> str:
        error_json: json = e.args[1]
        error_dict: dict = json.loads(error_json)
        return error_dict['error']['message']

    @staticmethod
    def debug(request: callable):
        try:
            return request()
        except RequestException as e:
            traceback.print_exc()
            raise e

    @staticmethod
    def suppress(request: callable, debug: bool = False):
        try:
            return request()
        except RequestException:
            if debug:
                traceback.print_exc()

    @staticmethod
    def handle(request: callable, handlers: dict[type(RequestException), callable], debug: bool = False):
        try:
            return HTTPErrorHelper.differentiate(request, debug)
        except RequestException as e:
            for exception, handler in handlers.items():
                if isinstance(e, exception):
                    return handler()

    @staticmethod
    def differentiate(request: callable, debug: bool = False):
        try:
            return request()
        except HTTPError as e:
            if debug:
                traceback.print_exc()
            error_message: str = HTTPErrorHelper.extract_message(e)
            match error_message:
                case "INVALID_EMAIL":
                    raise InvalidEmailException
                case "MISSING_PASSWORD":
                    raise MissingPasswordException
                case "INVALID_LOGIN_CREDENTIALS":
                    raise InvalidLoginCredentialsException
                case "EMAIL_EXISTS":
                    raise EmailExistsException
                case "EMAIL_NOT_FOUND":
                    raise EmailNotFoundException
                case "WEAK_PASSWORD : Password should be at least 6 characters":
                    raise WeakPasswordException
                case "Invalid HTTP method/URL pair.":
                    raise InvalidRequestException
                case _:
                    raise HTTPError


class InvalidEmailException(HTTPError):
    pass


class MissingPasswordException(HTTPError):
    pass


class InvalidLoginCredentialsException(HTTPError):
    pass


class EmailExistsException(HTTPError):
    pass


class EmailNotFoundException(HTTPError):
    pass


class WeakPasswordException(HTTPError):
    pass


class InvalidRequestException(HTTPError):
    pass

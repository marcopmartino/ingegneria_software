import json

from requests import HTTPError


class HTTPErrorHelper(object):

    @staticmethod
    def extract_message(e: HTTPError) -> str:
        error_json: json = e.args[1]
        error_dict: dict = json.loads(error_json)
        return error_dict['error']['message']

    @staticmethod
    def handle_request(request: callable):
        try:
            return request()
        except HTTPError as e:
            error_message: str = HTTPErrorHelper.extract_message(e)
            match error_message:
                case "INVALID_EMAIL":
                    raise InvalidEmailException
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


class EmailExistsException(HTTPError):
    pass


class EmailNotFoundException(HTTPError):
    pass


class WeakPasswordException(HTTPError):
    pass


class InvalidRequestException(HTTPError):
    pass

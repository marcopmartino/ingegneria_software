import json
import traceback

from PyQt5.QtWidgets import QMessageBox, QWidget
from requests import HTTPError, ConnectionError


class ErrorHelper:
    @staticmethod
    def debug(request: callable, exception_type: type(Exception) = Exception):
        try:
            return request()
        except exception_type as e:
            traceback.print_exc()
            raise e

    @staticmethod
    def suppress(request: callable, exception_type: type(Exception) = Exception, debug: bool = False):
        try:
            return request()
        except exception_type:
            if debug:
                traceback.print_exc()


class ConnectionErrorHelper(ErrorHelper):

    @staticmethod
    def handle(request: callable, parent: QWidget = None, show_dialog: bool = True, on_exception: callable = None):
        try:
            return request()
        except ConnectionError:
            if show_dialog:
                # Imposta e mostra il dialog
                QMessageBox.information(
                    parent,
                    "Connessione al database fallita",
                    "Connessione di rete assente: controlla la tua connessione a Internet e riprova.",
                    QMessageBox.Ok
                )
            if on_exception is not None:
                on_exception()


class HTTPErrorHelper(ErrorHelper):

    @staticmethod
    def extract_message(e: HTTPError) -> str:
        error_json: json = e.args[1]
        error_dict: dict = json.loads(error_json)
        return error_dict['error']['message']

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

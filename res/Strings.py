# Questo file contiene le codifiche di configurazione e le stringhe usate nell'applicazione

# Stringhe di configurazione
class Config:
    APPLICATION_NAME = "ShoeLastFactoryManager"
    APPLICATION_VERSION = "1.0.0"
    APPLICATION_VERSION_NAME = "First version"
    IMAGES_PATH = "res/images/"

    @staticmethod
    def image(filename):
        return f"url({Config.IMAGES_PATH + filename})"


# Stringhe usate nell'applicazione
# Access
class AccessStrings:
    BOTTOM_TEXT_LOGIN = "Non hai un account? Registrati"
    BOTTOM_TEXT_SIGN_UP = "Hai già un account? Accedi"
    LOGIN = 'Accedi'
    SING_UP = 'Registrati'
    TITLE_LOGIN = "Accedi al tuo account"
    TITLE_SIGN_UP = "Crea un nuovo account"


# Form
class FormStrings:
    COMPANY_NAME = "Nome azienda"
    DELIVERY_ADDRESS = "Indirizzo di recapito"
    EMAIL = "Email"
    IVA_NUMBER = "Partita IVA"
    NAME = "Nome"
    PASSWORD = "Password"
    PASSWORD_CONFIRM = "Conferma password"
    PHONE = "Telefono"
    SURNAME = "Cognome"


# Utility
class UtilityStrings:
    EMPTY = ""
    ERROR = "Errore"
    ERROR_EXTENDED = "Errore - Qualcosa è andato storto"
    ERROR_SHORTENED = "ERR"
    SPACE = " "
    LOADING = "Caricamento"
    LOADING_DOTS = "Caricamento..."
    LOADING_EXTENDED = "Caricamento in corso"
    LOADING_EXTENDED_DOTS = "Caricamento in corso..."
    WAIT = "Attendere"


# Valiadtion
class ValidationStrings:
    EMAIL_PASSWORD_WRONG = "Email e\\o password errati"
    EMAIL_ALREADY_USED = "Email già in uso"

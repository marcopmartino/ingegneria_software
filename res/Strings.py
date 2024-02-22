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
    SURNAME = "Cognome"
    EMAIL = "Email"
    NAME = "Nome"
    PASSWORD = "Password"


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

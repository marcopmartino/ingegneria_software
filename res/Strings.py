# Questo file contiene le codifiche di configurazione e le stringhe usate nell'applicazione

# Stringhe di configurazione
class Config:
    APPLICATION_NAME = "ShoeLastFactoryManager"
    APPLICATION_VERSION = "1.0.0"
    APPLICATION_VERSION_NAME = "First version"
    IMAGES_PATH = "res/images/"
    ICONS_PATH = "res/images/icons/"


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
    DESCRIPTION = "Descrizione"
    AMOUNT = "Importo"
    EMAIL = "Email"
    IVA_NUMBER = "Partita IVA"
    NAME = "Nome"
    PASSWORD = "Password"
    NEW_PASSWORD = "Nuova password"
    PASSWORD_CONFIRM = "Conferma password"
    NEW_PASSWORD_CONFIRM = "Conferma nuova password"
    PHONE = "Telefono"
    AGE = "Età"
    BIRTH_DATE = "Data di nascita"
    SURNAME = "Cognome"
    CF = "Codice fiscale"
    WORKER_TEXT = "Operaio"
    ADMIN_TEXT = "Manager"
    SAVE_EDIT = "Salva modifiche"
    DELETE_EDIT = "Annulla modifiche"


# OrderState
class OrderStateStrings:
    SENT = "Inviato"
    NOT_STARTED = "Non iniziato"
    STARTED = "Iniziato"
    PROCESSING = "In lavorazione"
    COMPLETED = "Completato"
    AWAITING_COLLECTION = "Da ritirare"
    DELIVERED = "Consegnato"


# PriceCatalog
class PriceCatalogStrings:
    FREE = "Gratuito"


# Profilo
class ProfileStrings:
    PROFILE = "PROFILO"
    PROFILE_DETAILS = "Dettagli profilo"
    EDIT_BUTTON = "Modifica profilo"
    DELETE_BUTTON = "Elimina profilo"


# Worker
class WorkerStrings:
    ADD_WORKER = "Aggiungi operaio"
    EDIT_WORKER = "Modifica operaio"


# Utility
class UtilityStrings:
    CHECK_INTERNET_CONNECTION = "Controllare la propria connessione a Internet"
    CONNECTION_ERROR = "Impossibile connettersi"
    NO_INTERNET_CONNECTION = "Connessione Internet assente"
    EMPTY = ""
    ERROR = "Errore"
    ERROR_SHORTENED = "ERR"
    ERROR_SOMETHING_WENT_WRONG = "Errore - Qualcosa è andato storto"
    SPACE = " "
    LOADING = "Caricamento"
    LOADING_DOTS = "Caricamento..."
    LOADING_ONGOING = "Caricamento in corso"
    LOADING_ONGOING_DOTS = "Caricamento in corso..."
    WAIT = "Attendere"


# Validation
class ValidationStrings:
    EMAIL_PASSWORD_WRONG = "Email e\\o password errati"
    EMAIL_ALREADY_USED = "Email già in uso"
    PASSWORD_CONFIRM_DIFFERENT = "Le due password non coincidono"
    FIELD_REQUIRED = "Campo richiesto"
    MIN_PASSWORD_ERROR = "La password deve essere lunga almeno 6 caratteri"

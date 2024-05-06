from pyrebase.pyrebase import Stream

from lib.firebaseData import Firebase


class CashRegisterNetwork:

    @staticmethod
    def stream(stream_handler: callable) -> Stream:
        return Firebase.database.child("cash_register").stream(stream_handler)

    @staticmethod
    def get_next_id():
        return Firebase.database.child("next_ids").get().val()["transaction"]

    @staticmethod
    def insert(data: dict) -> str:
        db = Firebase.database
        transaction_id: int = CashRegisterNetwork.get_next_id()
        serial_number: str = f"{transaction_id:04d}"

        # Inserisce la transazione e aggiorna il contatore
        db.child("cash_register").child("transactions").child(serial_number).set(data)
        db.child("next_ids").update({"transaction": transaction_id + 1})

        # Aggiorna la disponibilità di cassa
        cash_availability: float = db.child("cash_register").child("cash_availability").get().val()
        db.child("cash_register").child("cash_availability").set(cash_availability + data["amount"])
        return serial_number

    @staticmethod
    def update(transaction_id: str, data: dict):
        db = Firebase.database

        # Ottiene il nuovo importo
        new_amount: float = data["amount"]

        # Ottiene il vecchio importo
        old_amount: float = (db.child("cash_register").child("transactions")
                             .child(transaction_id).child("amount").get().val())

        # Aggiorna la transazione
        db.child("cash_register").child("transactions").child(transaction_id).update(data)

        # Aggiorna la disponibilità di cassa
        cash_availability: float = db.child("cash_register").child("cash_availability").get().val()
        db.child("cash_register").child("cash_availability").set(cash_availability + new_amount - old_amount)

    @staticmethod
    def delete(transaction_id: str):
        db = Firebase.database

        # Ottiene l'importo
        amount: float = (db.child("cash_register").child("transactions")
                         .child(transaction_id).child("amount").get().val())

        # Elimina la transazione
        db.child("cash_register").child("transactions").child(transaction_id).remove()

        # Aggiorna la disponibilità di cassa
        cash_availability: float = db.child("cash_register").child("cash_availability").get().val()
        db.child("cash_register").child("cash_availability").set(cash_availability - amount)

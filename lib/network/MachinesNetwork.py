from pyrebase.pyrebase import Stream

from lib.firebaseData import Firebase


class MachinesNetwork:

    @staticmethod
    def stream(stream_handler: callable) -> Stream:
        return Firebase.database.child("machines").stream(stream_handler)

    @staticmethod
    def update(machine_id: str, data: dict):
        Firebase.database.child("machines").child(machine_id).update(data)

from pyrebase.pyrebase import Stream

from lib.firebaseData import Firebase


class MachinesNetwork:

    @staticmethod
    def stream(stream_handler: callable) -> Stream:
        return Firebase.database.child("machines").stream(stream_handler)

    @staticmethod
    def update(machine_id: str, data: dict):
        Firebase.database.child("machines").child(machine_id).update(data)

    @staticmethod
    def request_to_manage_machine_output(machine_id: str):
        Firebase.database.child("machine_managers").child(machine_id).set(Firebase.auth.currentUserId())

    @staticmethod
    def can_manage_machine_output(machine_id: str) -> bool:
        return (Firebase.database.child("machine_managers").child(machine_id).get().val()
                == Firebase.auth.currentUserId())

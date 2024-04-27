from lib.firebaseData import firebase


class MachineNetwork:

    @staticmethod
    def stream(stream_handler: callable):
        firebase.database().child("machines").stream(stream_handler)

    @staticmethod
    def update(machine_id: str, data: dict):
        firebase.database().child("machines").child(machine_id).update(data)

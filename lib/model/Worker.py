
class Worker:

    def __init__(self, uid: str, name: str, CF: str, birth_date: str, mail: str, phone: str):
        super(Worker, self).__init__()
        self.uid = uid
        self.name = name
        self.CF = CF
        self.birth_date = birth_date
        self.mail = mail
        self.phone = phone

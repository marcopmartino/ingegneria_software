class User:

    def __init__(self, uid: str = None, phone: str = None, mail: str = None, role: str = None):
        super(User, self).__init__()
        self._uid = uid
        self._phone = phone
        self._mail = mail
        self._role = role

    def get_uid(self):
        return self._uid

    def get_role(self):
        return self._role



class User:

    def __init__(self, phone: str = None, mail: str = None, role: str = None):
        super(User, self).__init__()
        self.uid = None
        self.phone = phone
        self.mail = mail
        self.role = role

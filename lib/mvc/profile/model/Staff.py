class Staff:

    def __init__(self, uid: str = None, name: str = None, email: str = None,
                 phone: str = None, CF: str = None, birthDate: str = None, role: str = None):
        super(Staff, self).__init__()
        self.uid = uid
        self.name = name
        self.CF = CF
        self.birthDate = birthDate
        self.email = email
        self.phone = phone
        self.role = role

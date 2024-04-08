class Customer:

    def __init__(self, uid: str = None, companyName: str = None, email: str = None, phone: str = None,
                 delivery: str = None, IVA: str = None):
        super(Customer, self).__init__()
        self.uid = uid
        self.companyName = companyName
        self.email = email
        self.phone = phone
        self.delivery = delivery
        self.IVA = IVA


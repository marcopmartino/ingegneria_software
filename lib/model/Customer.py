class Customer:

    def __init__(self, company: str = None, phone: str = None, email: str = None,
                 delivery: str = None, IVA: str = None, role: str = None):
        super(Customer, self).__init__()
        self.company = company
        self.phone = phone
        self.email = email
        self.delivery = delivery
        self.IVA = IVA
        self.role = role

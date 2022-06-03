class Transaction():
    def __init__(self, from_address, to_address, amount): #from_address and to_address represent the public addresses and amount is the money transferred
        self.from_address = from_address
        self.to_address = to_address
        self.amount = amount
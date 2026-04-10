"""Transaction model stored during a session."""

class Transaction:
    def __init__(self, transaction_type, amount, from_account, to_account, name, account_number, misc=""):
        self.transaction_type = transaction_type
        self.amount = amount
        self.from_account = from_account
        self.to_account = to_account
        self.name = name
        self.account_number = account_number
        self.misc = misc
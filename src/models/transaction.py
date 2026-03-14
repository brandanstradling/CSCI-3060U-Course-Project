"""Transaction model stored during a session."""

from datetime import datetime



class Transaction:
    def __init__(self, transaction_type, amount, from_account, to_account, name, account_number, misc=""):
        self.transaction_type = transaction_type
        self.amount = amount
        self.from_account = from_account
        self.to_account = to_account
        self.name = name
        self.account_number = account_number
        self.misc = misc
        self.time = datetime.now()

    def log_transaction(self) -> str:
        """Return a formatted string for the transaction."""
        return (
            f"{self.transaction_type} {self.name} {self.account_number} "
            f"{self.amount:.2f} {self.misc}"
        )
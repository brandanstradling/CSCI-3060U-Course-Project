"""Account model used for lookups and basic in-memory updates."""

from src.config import TRANSACTION_FEES
from src.models.transaction import Transaction



class Account:
    def __init__(self, account_number, balance, name, status, plan="", total_transactions=0):
        self.account_number = account_number
        self.balance = balance
        self.name = name
        self.status = status  # "A" for active, "D" for disabled
        self.plan = plan
        self.total_transactions = total_transactions

    def disable(self):
        """Mark the account as inactive."""
        self.status = "D"

    def apply_backend_transaction(self, transaction: Transaction) -> bool:
        """
        Applies a transaction from the backend batch process, including fees.
        This method contains the core business logic for backend processing.
        Returns True on success, False on failure.
        """
        if self.status == 'D':
            # Do not process transactions on disabled accounts
            return False

        # Determine the fee based on the account plan for relevant transactions
        fee = 0.0
        if transaction.transaction_type in ("withdraw", "deposit", "transfer", "paybill"):
            fee = TRANSACTION_FEES.get(self.plan, 0.05)  # Default to SP fee

        # Apply transaction logic
        if transaction.transaction_type == "withdraw":
            if self.balance >= (transaction.amount + fee):
                self.balance -= (transaction.amount + fee)
                self.total_transactions += 1
                return True
            return False  # Insufficient funds

        elif transaction.transaction_type == "deposit":
            self.balance += (transaction.amount - fee)
            self.total_transactions += 1
            return True

        elif transaction.transaction_type == "transfer":
            # This method only handles the 'from' side of the transfer
            if self.balance >= (transaction.amount + fee):
                self.balance -= (transaction.amount + fee)
                self.total_transactions += 1
                return True
            return False  # Insufficient funds

        elif transaction.transaction_type == "changeplan":
            # The new plan should be in the transaction's misc field
            if transaction.misc in ('SP', 'NP'):
                self.plan = transaction.misc
                return True
            return False

        return False  # Unknown or unhandled transaction type

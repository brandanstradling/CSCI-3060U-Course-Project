"""Account model used for lookups and basic in-memory updates."""

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

        # Calculate daily transaction fee based on plan
        # Student plan (SP) = $0.05, Non-student (NP) = $0.10
        fee = 0.05 if self.plan == 'SP' else 0.10

        # Apply transaction logic
        if transaction.transaction_type == "withdraw":
            total_deduction = transaction.amount + fee
            if self.balance >= total_deduction:
                self.balance = round(self.balance - total_deduction, 2)
                self.total_transactions += 1
                return True
            return False  # Insufficient funds

        elif transaction.transaction_type == "deposit":
            if self.balance + transaction.amount >= fee:
                self.balance = round(self.balance + transaction.amount - fee, 2)
                self.total_transactions += 1
                return True
            return False  # Cannot afford fee on deposit

        elif transaction.transaction_type == "transfer":
            # This method only handles the 'from' side of the transfer
            total_deduction = transaction.amount + fee
            if self.balance >= total_deduction:
                self.balance = round(self.balance - total_deduction, 2)
                self.total_transactions += 1
                return True
            return False  # Insufficient funds

        elif transaction.transaction_type == "paybill":
            total_deduction = transaction.amount + fee
            if self.balance >= total_deduction:
                self.balance = round(self.balance - total_deduction, 2)
                self.total_transactions += 1
                return True
            return False  # Insufficient funds

        elif transaction.transaction_type == "changeplan":
            # The new plan should be in the transaction's misc field
            if transaction.misc in ('SP', 'NP') and self.balance >= fee:
                self.plan = transaction.misc
                self.balance = round(self.balance - fee, 2)
                self.total_transactions += 1
                return True
            return False

        return False  # Unknown or unhandled transaction type

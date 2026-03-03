"""Account model used for lookups and basic in-memory updates."""

from dataclasses import dataclass
from models.session import Session
from models.transaction import Transaction
from datetime import datetime



@dataclass


class Account:
    def __init__(self, account_number, balance, name, status):
        self.account_number = account_number
        self.balance = balance
        self.name = name
        self.status = status  # "A" for active, "I" for inactive

    def withdraw(self, amount: float) -> bool:
        """Withdraw from balance if it does not go negative."""
        if self.balance - amount < 0:
            return False
        self.balance -= amount
        return True

    def deposit(self, amount: float) -> Transaction:
        """Record a deposit and return a Transaction object."""
        transaction = Transaction(
            time=datetime.now(),
            transaction_type="deposit",
            amount=amount,
            FromAccount=0,
            ToAccount=self.account_number,
            name=self.name,
            account_number=self.account_number,
            misc=""
        )
        self.balance += amount
        return transaction

    def transfer(self, to_account: int, amount: float) -> Transaction:
        """Record a transfer. Returns a Transaction on success, None on failure."""
        if self.balance - amount < 0:
            return None  # Insufficient funds
        transaction = Transaction(
            time=datetime.now(),
            transaction_type="transfer",
            amount=amount,
            FromAccount=self.account_number,
            ToAccount=to_account,
            name=self.name,
            account_number=self.account_number,
            misc=""
        )
        self.balance -= amount
        return transaction

    def paybill(self, company: str, amount: float) -> Transaction:
        """Record a paybill transaction and return a Transaction object."""
        transaction = Transaction(
            time=datetime.now(),
            transaction_type="paybill",
            amount=amount,
            FromAccount=self.account_number,
            ToAccount=0,
            name=self.name,
            account_number=self.account_number,
            misc=company
        )
        self.balance -= amount
        return transaction

    def disable(self):
        """Mark the account as inactive."""
        self.status = "I"

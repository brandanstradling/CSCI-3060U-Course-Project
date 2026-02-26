"""Session state and per-session limit checks."""
# session.py: Tracks user sessions and enforces transaction limits
from dataclasses import dataclass
from typing import Optional
from typing import Union
from models.user import Admin, Standard
from models.transaction import Transaction


@dataclass



class Session:
    def __init__(self):
        self.active = False
        self.User = None
        self.withdrawal = 0.0
        self.transfer_total = 0.0
        self.paybill_total = 0.0

    def clearSession(self):
        """Reset the session state."""
        self.active = False
        self.User = None
        self.withdrawal = 0.0
        self.transfer_total = 0.0
        self.paybill_total = 0.0

    def login(self, user: Admin | Standard):
        """Start a new session for the given user."""
        self.clearSession()
        self.active = True
        self.User = user

    def logout(self):
        """End the current session."""
        self.clearSession()

    def isAdmin(self) -> bool:
        """Return True if the current user is an admin."""
        return isinstance(self.User, Admin)

    def withdrawal_limit(self, amount: float) -> bool:
        """Return True if a withdrawal amount is allowed in this session."""
        if self.isAdmin():
            return True
        return (self.withdrawal + amount) <= 500.00

    def transfer_limit(self, amount: float) -> bool:
        """Return True if a transfer amount is allowed in this session."""
        if self.isAdmin():
            return True
        return (self.transfer_total + amount) <= 1000.00

    def paybill_limit(self, amount: float) -> bool:
        """Return True if a paybill amount is allowed in this session."""
        if self.isAdmin():
            return True
        return (self.paybill_total + amount) <= 2000.00

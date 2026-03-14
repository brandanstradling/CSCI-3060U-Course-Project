"""Session state and per-session limit checks."""

from src.config import WITHDRAWAL_LIMIT, TRANSFER_LIMIT, PAYBILL_LIMIT
from src.models.user import Admin, Standard
from src.models.transaction import Transaction



class Session:
    def __init__(self):
        self.active = False
        self.user = None
        self.withdrawal = 0.0
        self.transfer_total = 0.0
        self.paybill_total = 0.0

    def clear_session(self):
        """Reset the session state."""
        self.active = False
        self.user = None
        self.withdrawal = 0.0
        self.transfer_total = 0.0
        self.paybill_total = 0.0

    def login(self, user: Admin | Standard):
        """Start a new session for the given user."""
        self.clear_session()
        self.active = True
        self.user = user

    def logout(self):
        """End the current session."""
        self.clear_session()

    def is_admin(self) -> bool:
        """Return True if the current user is an admin."""
        return isinstance(self.user, Admin)

    def withdrawal_limit(self, amount: float) -> bool:
        """Return True if a withdrawal amount is allowed in this session."""
        if self.is_admin():
            return True
        return (self.withdrawal + amount) <= WITHDRAWAL_LIMIT

    def transfer_limit(self, amount: float) -> bool:
        """Return True if a transfer amount is allowed in this session."""
        if self.is_admin():
            return True
        return (self.transfer_total + amount) <= TRANSFER_LIMIT

    def paybill_limit(self, amount: float) -> bool:
        """Return True if a paybill amount is allowed in this session."""
        if self.is_admin():
            return True
        return (self.paybill_total + amount) <= PAYBILL_LIMIT

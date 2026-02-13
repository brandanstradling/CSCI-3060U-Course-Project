"""Session state and per-session limit checks."""

from dataclasses import dataclass
from typing import Optional

from .user import Admin, User


@dataclass
class Session:
    """Tracks who is logged in and enforces per-session limits."""

    active: bool = False
    User: Optional[User] = None
    withdrawal: float = 0.0
    transfer_total: float = 0.0
    paybill_total: float = 0.0

    def clearSession(self, active: bool) -> None:
        """Reset the session state."""
        self.active = active
        self.User = None
        self.withdrawal = 0.0
        self.transfer_total = 0.0
        self.paybill_total = 0.0

    def login(self, active: bool, user: User) -> None:
        """Start a new session for the given user."""
        self.active = active
        self.User = user
        self.withdrawal = 0.0
        self.transfer_total = 0.0
        self.paybill_total = 0.0

    def logout(self, active: bool) -> None:
        """End the current session."""
        self.clearSession(active=active)

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

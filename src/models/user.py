"""User roles used to represent standard and admin sessions."""

from dataclasses import dataclass
from datetime import datetime

from src.models.transaction import Transaction


@dataclass
class User:
    """Base user role with a simple login-eligibility check."""

    password: str = ""

    def verify_login(self, session_active: bool) -> bool:
        """Return True if login is allowed given the current session state."""
        return not session_active


@dataclass
class Standard(User):
    """Standard (non-privileged) session identity."""

    account_username: str = ""
    account_number: int = 0


@dataclass
class Admin(User):
    """Admin (privileged) session identity."""

    admin_ID: str = ""

    def create(self, Name: str, Amount: float) -> Transaction:
        """Build a Transaction object representing a create request."""
        return Transaction(
            transaction_type="create",
            amount=Amount,
            from_account=0,
            to_account=0,
            name=Name,
            account_number=0,
            misc="",
        )

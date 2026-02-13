"""Transaction model stored during a session."""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Transaction:
    """Stores the details of one requested transaction."""

    time: datetime
    transaction_type: str
    amount: float
    FromAccount: int
    ToAccount: int
    name: str = ""
    account_number: int = 0
    misc: str = ""

    def log_transaction(self) -> str:
        """Return a readable representation of the transaction."""
        return (
            f"{self.transaction_type} {self.name} {self.account_number} "
            f"{self.amount:.2f} {self.misc}"
        )

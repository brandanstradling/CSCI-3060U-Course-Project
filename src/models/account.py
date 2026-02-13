"""Account model used for lookups and basic in-memory updates."""

from dataclasses import dataclass


@dataclass
class Account:
    """Represents a single bank account record."""
    account_number: int
    balance: float
    account_holder_name: str
    account_plan: str = "NP"
    account_status: bool = True  # True = active, False = disabled
    account_type: str = ""

    def withdraw(self, amount: float) -> bool:
        """Withdraw from balance if it does not go negative."""
        if (self.balance - amount) < 0.0:
            return False
        self.balance -= amount
        return True

    def transfer(self, account_holder_name: str, account_number: int, amount: float) -> None:
        """Placeholder for transfer-related account updates."""
        return

    def paybill(
        self, account_holder_name: str, account_number: int, amount: float, company_name: str
    ) -> None:
        """Placeholder for paybill-related account updates."""
        return

    def deposit(self, amount: float) -> None:
        """Placeholder for deposit-related account updates."""
        return

    def delete(self) -> None:
        """Mark the account as inactive."""
        self.account_status = False

    def disable(self) -> None:
        """Disable the account."""
        self.account_status = False

    def changeplan(self) -> None:
        """Change the account plan to non-student (NP)."""
        self.account_plan = "NP"

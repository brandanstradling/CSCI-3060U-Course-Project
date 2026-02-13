"""Console controller for the interactive front end."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Tuple

from io.accounts_file import load_current_accounts
from io.transactions_file import write_daily_transaction_file
from models.account import Account
from models.session import Session
from models.transaction import Transaction
from models.user import Admin, Standard, User

PAYBILL_COMPANIES = {"EC", "CQ", "FI"}  # Allowed paybill company codes.


@dataclass
class FrontEndApp:
    """Runs the command loop, validates inputs, and logs transactions."""

    current_accounts_path: str
    daily_transactions_path: str
    session: Session = field(default_factory=Session)
    accounts_by_num: Dict[int, Account] = field(default_factory=dict)
    logged_transactions: List[Transaction] = field(default_factory=list)

    def run(self) -> None:
        """Read commands from stdin and dispatch to handlers."""
        while True:
            cmd = input().strip().lower()

            if cmd == "login":
                self._handle_login()
            elif cmd == "logout":
                self._handle_logout()
            elif cmd == "withdrawal":
                self._handle_withdrawal()
            elif cmd == "transfer":
                self._handle_transfer()
            elif cmd == "paybill":
                self._handle_paybill()
            elif cmd == "deposit":
                self._handle_deposit()
            elif cmd == "create":
                self._handle_create()
            elif cmd == "delete":
                self._handle_delete()
            elif cmd == "disable":
                self._handle_disable()
            elif cmd == "changeplan":
                self._handle_changeplan()
            else:
                print("Invalid transaction.")

    def _require_login(self) -> bool:
        """Return True if a session is active, otherwise print an error."""
        if not self.session.active:
            print("Please login first.")
            return False
        return True

    def _require_admin(self) -> bool:
        """Return True if the current session is an admin session."""
        if not self._require_login():
            return False
        if not self.session.isAdmin():
            print("Admin privileges required.")
            return False
        return True

    def _prompt_amount(self, prompt: str) -> float:
        """Prompt for an amount and return 0.0 on invalid input."""
        raw = input(prompt).strip()
        try:
            return float(raw)
        except ValueError:
            print("Invalid amount.")
            return 0.0

    def _prompt_int(self, prompt: str) -> int:
        """Prompt for an integer and return 0 on invalid input."""
        raw = input(prompt).strip()
        try:
            return int(raw)
        except ValueError:
            print("Invalid number.")
            return 0

    def _get_name_and_account_number(self) -> Tuple[str, int]:
        """Return (account_holder_name, account_number) based on session mode."""
        if self.session.isAdmin():
            name = input("Account holder name: ").strip()
            acct = self._prompt_int("Account number: ")
            return name, acct

        assert isinstance(self.session.User, Standard)
        acct = self._prompt_int("Account number: ")
        return self.session.User.account_username, acct

    def _handle_login(self) -> None:
        """Start a session and load the current accounts file."""
        temp_user = User()
        if not temp_user.verifyLogin(self.session.active):
            print("Already logged in.")
            return

        mode = input("Session type (standard/admin): ").strip().lower()
        if mode not in ("standard", "admin"):
            print("Invalid session type.")
            return

        if mode == "standard":
            name = input("Account holder name: ").strip()
            user: User = Standard(account_username=name, account_number=0)
        else:
            admin_id = input("Admin ID (optional): ").strip()
            user = Admin(admin_ID=admin_id)

        self.accounts_by_num = load_current_accounts(self.current_accounts_path)
        self.session.login(active=True, user=user)
        self.logged_transactions.clear()
        print("Login successful.")

    def _handle_logout(self) -> None:
        """Write the daily transaction file and end the session."""
        if not self._require_login():
            return

        write_daily_transaction_file(
            self.daily_transactions_path,
            self.logged_transactions,
        )
        self.session.logout(active=False)
        self.logged_transactions.clear()
        print("Logged out.")

    def _handle_withdrawal(self) -> None:
        """Prompt for withdrawal details, enforce limits, and log the transaction."""
        if not self._require_login():
            return

        name, acct = self._get_name_and_account_number()
        amt = self._prompt_amount("Withdraw amount: ")

        if not self.session.withdrawal_limit(amt):
            print("Withdrawal limit exceeded.")
            return

        t = Transaction(
            time=datetime.now(),
            transaction_type="withdrawal",
            amount=amt,
            FromAccount=acct,
            ToAccount=0,
            name=name,
            account_number=acct,
            misc="",
        )
        self.logged_transactions.append(t)
        self.session.withdrawal += amt
        print("Withdrawal recorded.")

    def _handle_transfer(self) -> None:
        """Prompt for transfer details, enforce limits, and log the transaction."""
        if not self._require_login():
            return

        name, from_acct = self._get_name_and_account_number()
        to_acct = self._prompt_int("To account number: ")
        amt = self._prompt_amount("Transfer amount: ")

        if not self.session.transfer_limit(amt):
            print("Transfer limit exceeded.")
            return

        t = Transaction(
            time=datetime.now(),
            transaction_type="transfer",
            amount=amt,
            FromAccount=from_acct,
            ToAccount=to_acct,
            name=name,
            account_number=from_acct,
            misc="",
        )
        self.logged_transactions.append(t)
        self.session.transfer_total += amt
        print("Transfer recorded (prototype).")

    def _handle_paybill(self) -> None:
        """Prompt for bill details, validate company code, enforce limits, and log the transaction."""
        if not self._require_login():
            return

        name, acct = self._get_name_and_account_number()
        company = input("Company code (EC/CQ/FI): ").strip().upper()
        amt = self._prompt_amount("Paybill amount: ")

        if company not in PAYBILL_COMPANIES:
            print("Invalid company.")
            return

        if not self.session.paybill_limit(amt):
            print("Paybill limit exceeded.")
            return

        t = Transaction(
            time=datetime.now(),
            transaction_type="paybill",
            amount=amt,
            FromAccount=acct,
            ToAccount=0,
            name=name,
            account_number=acct,
            misc=company,
        )
        self.logged_transactions.append(t)
        self.session.paybill_total += amt
        print("Paybill recorded.")

    def _handle_deposit(self) -> None:
        """Prompt for deposit details and log the transaction."""
        if not self._require_login():
            return

        name, acct = self._get_name_and_account_number()
        amt = self._prompt_amount("Deposit amount: ")

        t = Transaction(
            time=datetime.now(),
            transaction_type="deposit",
            amount=amt,
            FromAccount=acct,
            ToAccount=0,
            name=name,
            account_number=acct,
            misc="",
        )
        self.logged_transactions.append(t)
        print("Deposit recorded.")

    def _handle_create(self) -> None:
        """Prompt for create details and log the transaction."""
        if not self._require_admin():
            return

        name = input("New account holder name: ").strip()
        amt = self._prompt_amount("Initial balance: ")

        t = Transaction(
            time=datetime.now(),
            transaction_type="create",
            amount=amt,
            FromAccount=0,
            ToAccount=0,
            name=name,
            account_number=0,
            misc="",
        )
        self.logged_transactions.append(t)
        print("Create recorded.")

    def _handle_delete(self) -> None:
        """Prompt for delete details and log the transaction."""
        if not self._require_admin():
            return

        name = input("Account holder name: ").strip()
        acct = self._prompt_int("Account number: ")

        t = Transaction(
            time=datetime.now(),
            transaction_type="delete",
            amount=0.0,
            FromAccount=acct,
            ToAccount=0,
            name=name,
            account_number=acct,
            misc="",
        )
        self.logged_transactions.append(t)
        print("Delete recorded.")

    def _handle_disable(self) -> None:
        """Prompt for disable details and log the transaction."""
        if not self._require_admin():
            return

        name = input("Account holder name: ").strip()
        acct = self._prompt_int("Account number: ")

        t = Transaction(
            time=datetime.now(),
            transaction_type="disable",
            amount=0.0,
            FromAccount=acct,
            ToAccount=0,
            name=name,
            account_number=acct,
            misc="",
        )
        self.logged_transactions.append(t)
        print("Disable recorded.")

    def _handle_changeplan(self) -> None:
        """Prompt for changeplan details and log the transaction."""
        if not self._require_admin():
            return

        name = input("Account holder name: ").strip()
        acct = self._prompt_int("Account number: ")

        t = Transaction(
            time=datetime.now(),
            transaction_type="changeplan",
            amount=0.0,
            FromAccount=acct,
            ToAccount=0,
            name=name,
            account_number=acct,
            misc="",
        )
        self.logged_transactions.append(t)
        print("Changeplan recorded.")

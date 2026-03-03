"""Console controller for the interactive front end."""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple
import sys

from file_io.accounts_file import load_current_accounts
from file_io.transactions_file import write_daily_transaction_file
from models.account import Account
from models.session import Session
from models.transaction import Transaction
from models.user import Admin, Standard

PAYBILL_COMPANIES = {"EC", "CQ", "FI"}


@dataclass
class FrontEndApp:
    current_accounts_path: str
    daily_transactions_path: str
    session: Session = field(default_factory=Session)
    accounts_by_num: Dict[int, Account] = field(default_factory=dict)
    logged_transactions: List[Transaction] = field(default_factory=list)

    def _print(self, msg: str) -> None:
        # user-facing messages go to stderr so tests (stdout) are unaffected
        print(msg, file=sys.stderr)

    def run(self) -> None:
        # initial banner
        self._print("Welcome to the banking system. Enter commands or EOF to quit.")
        while True:
            try:
                self._print("Command (withdrawal, transfer, paybill, deposit, balance, create, delete, disable, changeplan, login, logout):")
                cmd = input().strip().lower()
            except EOFError:
                self._print("Goodbye.")
                return

            # aliases to match tests/spec variants
            if cmd == "withdraw":
                cmd = "withdrawal"

            if cmd == "login":
                self._handle_login()
            elif cmd == "logout":
                self._handle_logout()
                self._print("Goodbye.")
                return
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
            elif cmd == "balance":
                self._handle_balance()
            else:
                print("Invalid transaction.")

    def _require_login(self) -> bool:
        if not self.session.active:
            print("Please login first.")
            return False
        return True

    def _require_admin(self) -> bool:
        if not self._require_login():
            return False
        if not self.session.isAdmin():
            print("Admin privileges required.")
            return False
        return True

    def _prompt_amount(self) -> float:
        self._print("Amount:")
        raw = input().strip()
        try:
            return float(raw)
        except ValueError:
            print("Invalid amount.")
            return 0.0

    def _prompt_int(self) -> int:
        self._print("Enter number:")
        raw = input().strip()
        try:
            return int(raw)
        except ValueError:
            print("Invalid number.")
            return 0

    def _get_name_and_account_number(self) -> Tuple[str, int]:
        if self.session.isAdmin():
            self._print("Name:")
            name = input().strip()
            acct = self._prompt_int()
            return name, acct

        assert isinstance(self.session.User, Standard)
        acct = self._prompt_int()
        return self.session.User.account_username, acct

    def _handle_login(self) -> None:
        if self.session.active:
            print("Already logged in.")
            return

        self._print("Session type (standard/admin):")
        mode = input().strip().lower()
        if mode not in ("standard", "admin"):
            print("Invalid session type.")
            return

        if mode == "standard":
            self._print("Name:")
            name = input().strip()
            acct = self._prompt_int()
            self._print("Password:")
            pwd = input().strip()
            user = Standard(account_username=name, account_number=acct, password=pwd)
        else:
            self._print("Admin ID:")
            admin_id = input().strip()
            user = Admin(admin_ID=admin_id)

        if not user.verifyLogin(self.session.active):
            print("Invalid credentials.")
            return

        self.accounts_by_num = {a.account_number: a for a in load_current_accounts(self.current_accounts_path)}
        self.session.login(user=user)
        self.logged_transactions.clear()

        # Don't log login transactions
        print("Login successful. ")

    def _handle_logout(self) -> None:
        if not self._require_login():
            return
        write_daily_transaction_file(self.daily_transactions_path, self.logged_transactions)
        self.session.logout()
        self.logged_transactions.clear()
        print("Logged out.")

    def _handle_withdrawal(self) -> None:
        if not self._require_login():
            return

        name, acct = self._get_name_and_account_number()
        if acct not in self.accounts_by_num:
            print("Account does not exist.")
            return

        amt = self._prompt_amount()
        if not self.session.withdrawal_limit(amt):
            print("Withdrawal limit exceeded.")
            return

        t = Transaction("withdraw", amt, 0, 0, name, acct, "")
        self.logged_transactions.append(t)
        self.session.withdrawal += amt
        print("Withdrawal recorded. ")

    def _handle_transfer(self) -> None:
        if not self._require_login():
            return

        name, from_acct = self._get_name_and_account_number()
        self._print("Destination account:")
        to_acct = self._prompt_int()

        if from_acct not in self.accounts_by_num or to_acct not in self.accounts_by_num:
            print("Account does not exist.")
            return

        amt = self._prompt_amount()
        if not self.session.transfer_limit(amt):
            print("Transfer limit exceeded.")
            return

        t = Transaction("transfer", amt, from_acct, to_acct, name, from_acct, "")
        self.logged_transactions.append(t)
        self.session.transfer_total += amt
        print("Transfer recorded (prototype). ")

    def _handle_paybill(self) -> None:
        if not self._require_login():
            return

        name, acct = self._get_name_and_account_number()
        if acct not in self.accounts_by_num:
            print("Account does not exist.")
            return

        self._print("Company code (EC/CQ/FI):")
        company = input().strip().upper()
        amt = self._prompt_amount()

        if company not in PAYBILL_COMPANIES:
            print("Invalid company.")
            return
        if not self.session.paybill_limit(amt):
            print("Paybill limit exceeded.")
            return

        # Your expected shows ToAccount: EC/CQ/FI, so put company there
        t = Transaction("paybill", amt, acct, company, name, acct, "")
        self.logged_transactions.append(t)
        self.session.paybill_total += amt
        print("Paybill recorded. ")

    def _handle_deposit(self) -> None:
        if not self._require_login():
            return

        name, acct = self._get_name_and_account_number()
        if acct not in self.accounts_by_num:
            print("Account does not exist.")
            return

        amt = self._prompt_amount()
        t = Transaction("deposit", amt, 0, 0, name, acct, "")
        self.logged_transactions.append(t)
        self.accounts_by_num[acct].balance += amt
        print("Deposit recorded. ")

    def _handle_create(self) -> None:
        if not self._require_admin():
            return

        self._print("Name:")
        name = input().strip()
        acct = self._prompt_int()
        amt = self._prompt_amount()

        t = Transaction("create", 0.0, 0, 0, name, acct, "")
        self.logged_transactions.append(t)
        print("Create recorded.")

    def _handle_delete(self) -> None:
        if not self._require_admin():
            return

        self._print("Name:")
        name = input().strip()
        acct = self._prompt_int()

        if acct not in self.accounts_by_num:
            print("Account does not exist.")
            return

        t = Transaction("delete", 0.0, 0, 0, name, acct, "")
        self.logged_transactions.append(t)
        del self.accounts_by_num[acct]
        print("Delete recorded.")

    def _handle_disable(self) -> None:
        if not self._require_admin():
            return

        self._print("Name:")
        name = input().strip()
        acct = self._prompt_int()

        if acct not in self.accounts_by_num:
            print("Account does not exist.")
            return

        t = Transaction("disable", 0.0, 0, 0, name, acct, "")
        self.logged_transactions.append(t)
        self.accounts_by_num[acct].status = "disabled"
        print("Disable recorded.")

    def _handle_changeplan(self) -> None:
        if not self._require_admin():
            return

        self._print("Name:")
        name = input().strip()
        acct = self._prompt_int()

        if acct not in self.accounts_by_num:
            print("Account does not exist.")
            return

        t = Transaction("changeplan", 0.0, 0, 0, name, acct, "")
        self.logged_transactions.append(t)
        self.accounts_by_num[acct].plan = "new_plan"
        print("Changeplan recorded.")

    def _handle_balance(self) -> None:
        if not self._require_login():
            return

        name, acct = self._get_name_and_account_number()
        if acct not in self.accounts_by_num:
            print("Account does not exist.")
            return

        bal = float(self.accounts_by_num[acct].balance)
        t = Transaction("balance", 0.0, 0, 0, name, acct, "")
        self.logged_transactions.append(t)
        print(f"Balance: {bal:.2f} ")
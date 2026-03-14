"""IO writers for accounts and transactions."""

from typing import List
from src.config import FIXED_TIME_STR
from src.models.account import Account
from src.models.transaction import Transaction


def write_master_accounts_file(accounts: List[Account], file_path: str):
    """
    Writes the new Master Accounts File in the fixed-width format.
    Format: NNNNN AAAAAAAAAAAAAAAAAAAA S BBBBBB.BB TTTT PL
    """
    with open(file_path, 'w') as file:
        for acc in accounts:
            acc_num = str(acc.account_number).zfill(5)
            name = acc.name.ljust(20)
            status = acc.status
            balance = f"{acc.balance:08.2f}"
            transactions = str(acc.total_transactions).zfill(4)
            plan = acc.plan.ljust(2)

            line = f"{acc_num} {name}{status} {balance} {transactions} {plan}\n"
            file.write(line)


def write_current_accounts_file(accounts: List[Account], file_path: str):
    """
    Writes the new Current Bank Accounts File.
    Format: NNNNN AAAAAAAAAAAAAAAAAAAA S BBBBBB.BB
    """
    with open(file_path, 'w') as file:
        for acc in accounts:
            # Basic validation before writing
            if acc.account_number > 99999:
                raise ValueError(f"Account number exceeds 5 digits: {acc.account_number}")
            if acc.balance > 99999.99:
                raise ValueError(f"Balance exceeds maximum $99999.99: {acc.balance}")

            # Format fields
            acc_num = str(acc.account_number).zfill(5)
            name = acc.name.ljust(20)
            status = acc.status
            balance = f"{acc.balance:08.2f}"

            line = f"{acc_num}{name}{status}{balance}\n"
            file.write(line)

        # Add ENDOFFILE marker
        file.write("00000ENDOFFILE          A00000.00\n")


def write_daily_transaction_file(path: str, transactions: List[Transaction]) -> None:
    """Write transactions in the multi-line expected (.etf) format."""
    # Use newline='' to prevent Python from converting \n to \r\n on Windows
    with open(path, "w", encoding="utf-8", newline="") as f:
        for t in transactions:
            # Match the expected formatting exactly
            f.write(f"Transaction: {t.transaction_type}\n")
            f.write(f"Amount: {float(t.amount)}\n")

           # FromAccount: pad if non-zero, don't pad if zero
            from_acct = int(t.from_account) if t.from_account else 0
            if from_acct > 0:
                f.write(f"FromAccount: {from_acct:05d}\n")
            else:
                f.write(f"FromAccount: {from_acct}\n")

            # ToAccount: handle string (company) and numeric cases
            if isinstance(t.to_account, str):
                # Company name for paybill
                f.write(f"ToAccount: {t.to_account}\n")
            else:
                # Numeric account: pad if non-zero, don't pad if zero
                to_acct = int(t.to_account) if t.to_account else 0
                if to_acct > 0:
                    f.write(f"ToAccount: {to_acct:05d}\n")
                else:
                    f.write(f"ToAccount: {to_acct}\n")

            f.write(f"Name: {t.name}\n")

            # Expected shows 5-digit account number (00001)
            try:
                acct_num = int(t.account_number)
            except Exception:
                acct_num = 0
            f.write(f"Account_Number: {acct_num:05d}\n")

            # Per expected format, Misc field is on its own line without a value.
            f.write("Misc:\n")
            f.write(f"Time: {FIXED_TIME_STR}\n")
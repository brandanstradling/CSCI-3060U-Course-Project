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
    # Sort accounts by account number to satisfy ascending order constraint
    accounts = sorted(accounts, key=lambda a: a.account_number)

    with open(file_path, 'w', newline='\n') as file:
        for acc in accounts:
            # Validation
            if not isinstance(acc.account_number, int) or acc.account_number < 0 or acc.account_number > 99999:
                raise ValueError(f"Invalid account number: {acc.account_number}")
            if not isinstance(acc.balance, (int, float)) or acc.balance < 0:
                raise ValueError(f"Invalid balance: {acc.balance}")
            if acc.status not in ('A', 'D'):
                raise ValueError(f"Invalid account status: {acc.status}")
            if len(acc.name) > 20:
                raise ValueError(f"Account name too long: {acc.name}")
            if not isinstance(acc.total_transactions, int) or acc.total_transactions < 0:
                raise ValueError(f"Invalid transaction count: {acc.total_transactions}")
            if acc.plan not in ('', 'SP', 'NP'):
                raise ValueError(f"Invalid account plan: {acc.plan}")

            # Format fields
            acc_num = str(acc.account_number).zfill(5)
            name = acc.name.ljust(20)
            status = acc.status
            balance = f"{acc.balance:08.2f}"
            transactions = str(acc.total_transactions).zfill(4)
            plan = acc.plan.ljust(2)

            line = f"{acc_num} {name} {status} {balance} {transactions} {plan}\n"
            file.write(line)


def write_current_accounts_file(accounts: List[Account], file_path: str):
    """
    Writes the new Current Bank Accounts File.
    Format: NNNNN AAAAAAAAAAAAAAAAAAAA S BBBBBB.BB
    """
    # Sort accounts by account number ascending
    accounts = sorted(accounts, key=lambda a: a.account_number)

    with open(file_path, 'w', newline='\n') as file:
        for acc in accounts:
            # Basic validation before writing
            if not isinstance(acc.account_number, int) or acc.account_number < 0 or acc.account_number > 99999:
                raise ValueError(f"Invalid account number: {acc.account_number}")
            if not isinstance(acc.balance, (int, float)) or acc.balance < 0 or acc.balance > 999999.99:
                raise ValueError(f"Invalid balance: {acc.balance}")
            if acc.status not in ('A', 'D'):
                raise ValueError(f"Invalid account status: {acc.status}")
            if len(acc.name) > 20:
                raise ValueError(f"Account name too long: {acc.name}")

            # Format fields
            acc_num = str(acc.account_number).zfill(5)
            name = acc.name.ljust(20)
            status = acc.status
            balance = f"{acc.balance:08.2f}"

            line = f"{acc_num} {name} {status} {balance}\n"
            file.write(line)

        # Add ENDOFFILE marker
        file.write("00000 ENDOFFILE           A 00000.00\n")


def write_daily_transaction_file(path: str, transactions: List[Transaction]) -> None:
    """Write transactions in the 40-character fixed-width format."""
    TYPE_TO_CODE = {
        'withdraw': '01',
        'transfer': '02',
        'paybill': '03',
        'deposit': '04',
        'create': '05',
        'delete': '06',
        'disable': '07',
        'changeplan': '08',
    }

    with open(path, "w", encoding="utf-8", newline="\n") as f:
        for t in transactions:
            if t.transaction_type == 'balance':
                continue  # Do not record balance inquiries in the daily file

            code = TYPE_TO_CODE.get(t.transaction_type, '00')
            name = str(t.name).ljust(20, ' ')[:20]
            
            try:
                acct_num = int(t.account_number)
            except (ValueError, TypeError):
                acct_num = 0
            acct_str = f"{acct_num:05d}"
            
            try:
                amt = float(t.amount)
            except (ValueError, TypeError):
                amt = 0.0
            amt_str = f"{amt:08.2f}"
            
            misc = str(t.misc).ljust(2, ' ')[:2]
            
            # Format: CC AAAAAAAAAAAAAAAAAAAA NNNNN PPPPPPPPMM (Length: 40)
            # To support transfers despite spec limitations, append destination account
            if t.transaction_type == 'transfer':
                try:
                    to_acct = int(t.to_account)
                except (ValueError, TypeError):
                    to_acct = 0
                line = f"{code} {name} {acct_str} {amt_str}{misc} {to_acct:05d}\n"
            else:
                line = f"{code} {name} {acct_str} {amt_str}{misc}\n"
                
            f.write(line)
        
        # Append end of session marker to session file
        f.write("00                                      \n")
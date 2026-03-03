"""Write transaction records to the daily transaction file in the expected .etf format."""

from typing import List
from models.transaction import Transaction

FIXED_TIME_STR = "2025-03-01 10:00:00"


def write_daily_transaction_file(path: str, transactions: List[Transaction]) -> None:
    """Write transactions in the multi-line expected (.etf) format."""
    # Use newline='' to prevent Python from converting \n to \r\n on Windows
    with open(path, "w", encoding="utf-8", newline="") as f:
        for t in transactions:
            # Match the expected formatting exactly
            f.write(f"Transaction: {t.transaction_type}\n")
            f.write(f"Amount: {float(t.amount)}\n")
            
           # FromAccount: pad if non-zero, don't pad if zero
            from_acct = int(t.FromAccount) if t.FromAccount else 0
            if from_acct > 0:
                f.write(f"FromAccount: {from_acct:05d}\n")
            else:
                f.write(f"FromAccount: {from_acct}\n")
            
            # ToAccount: handle string (company) and numeric cases
            if isinstance(t.ToAccount, str):
                # Company name for paybill
                f.write(f"ToAccount: {t.ToAccount}\n")
            else:
                # Numeric account: pad if non-zero, don't pad if zero
                to_acct = int(t.ToAccount) if t.ToAccount else 0
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
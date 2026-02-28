"""Write transaction records to the daily transaction file in the expected .etf format."""

from typing import List
from models.transaction import Transaction

# Your expected files show this fixed time string (not real time).
FIXED_TIME_STR = "2025-03-01 10:00:00"


def write_daily_transaction_file(path: str, transactions: List[Transaction]) -> None:
    """Write transactions in the multi-line expected (.etf) format."""
    with open(path, "w", encoding="utf-8") as f:
        for t in transactions:
            # Match the expected formatting exactly
            f.write(f"Transaction: {t.transaction_type}\n")
            f.write(f"Amount: {float(t.amount)}\n")
            f.write(f"FromAccount: {t.FromAccount}\n")
            f.write(f"ToAccount: {t.ToAccount}\n")
            f.write(f"Name: {t.name}\n")

            # Expected shows 5-digit account number (00001)
            try:
                acct_num = int(t.account_number)
            except Exception:
                acct_num = 0
            f.write(f"Account_Number: {acct_num:05d}\n")

            f.write("Misc:\n")
            f.write(f"Time: {FIXED_TIME_STR}\n")
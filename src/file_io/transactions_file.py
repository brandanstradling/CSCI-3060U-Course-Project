"""Format and write transaction records to the daily transaction file."""

from datetime import datetime
from typing import List

from models.transaction import Transaction
from .formats import NAME_W, ACCT_W, AMT_W, MISC_W, LINE_W, left, zfill_int, money


def tx_code(transaction_type: str) -> str:
    """Convert a transaction type string to its 2-digit code."""
    mapping = {
        "withdrawal": "01",
        "transfer": "02",
        "paybill": "03",
        "deposit": "04",
        "create": "05",
        "delete": "06",
        "disable": "07",
        "changeplan": "08",
        "end": "00",
    }
    return mapping[transaction_type]


def format_daily_record(t: Transaction) -> str:
    """Format a Transaction into a fixed-width output line."""
    core = (
        tx_code(t.transaction_type)
        + left(t.name, NAME_W)
        + zfill_int(t.account_number, ACCT_W)
        + money(t.amount, AMT_W)
        + left(t.misc, MISC_W)
    )
    return core.ljust(LINE_W, " ")[:LINE_W]


def write_daily_transaction_file(path: str, transactions: List[Transaction]) -> None:
    """Write all transactions plus a final end-of-session record."""
    with open(path, "w", encoding="utf-8") as f:
        for t in transactions:
            f.write(format_daily_record(t) + "\n")

        end = Transaction(
            time=datetime.now(),
            transaction_type="end",
            amount=0.0,
            FromAccount=0,
            ToAccount=0,
            name="",
            account_number=0,
            misc="",
        )
        f.write(format_daily_record(end) + "\n")

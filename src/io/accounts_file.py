"""Load Account objects from the current accounts file."""

from typing import Dict, Optional

from models.account import Account


def parse_current_account_line(line: str) -> Optional[Account]:
    """Parse one fixed-width account line, returning None for the end sentinel."""
    line = line.rstrip("\n")

    acct_num = int(line[0:5])
    name = line[5:25].rstrip()
    status = line[25:26]
    balance = float(line[26:34])

    if name.strip() == "ENDOFFILE":
        return None

    active = (status == "A")
    return Account(
        account_number=acct_num,
        balance=balance,
        account_holder_name=name,
        account_status=active,
    )


def load_current_accounts(path: str) -> Dict[int, Account]:
    """Load all accounts into a dict keyed by account number."""
    accounts: Dict[int, Account] = {}

    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            acc = parse_current_account_line(raw)
            if acc is None:
                break
            accounts[acc.account_number] = acc

    return accounts

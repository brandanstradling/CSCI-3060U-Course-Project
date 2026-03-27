"""IO readers for accounts and transactions."""

from typing import Dict, List, Optional
from src.models.account import Account
from src.models.transaction import Transaction
from src.backend.utils.print_error import log_constraint_error


def parse_current_account_line(line: str) -> Optional[Account]:
    """Parse one fixed-width current account line, returning None for the end sentinel."""
    line = line.rstrip("\n")

    # Check for end-of-file marker before parsing
    if "ENDOFFILE" in line:
        return None

    if len(line) not in (34, 35):
        return None

    acct_num = int(line[0:5])
    name = line[5:25].rstrip()
    status = line[25:26]

    # Support both exact 34-char and 35-char current account formats
    if len(line) == 34:
        balance_str = line[26:34]
    else:
        balance_str = line[27:35]

    balance = float(balance_str)

    return Account(
        account_number=acct_num,
        balance=balance,
        name=name,
        status=status,
    )


def load_current_accounts(path: str) -> List[Account]:
    """Load all current accounts into a list."""
    accounts = []

    try:
        with open(path, "r", encoding="utf-8") as f:
            for raw in f:
                acc = parse_current_account_line(raw)
                if acc is None:
                    break
                accounts.append(acc)
    except FileNotFoundError:
        log_constraint_error(f"File not found: {path}", "File I/O", fatal=True)

    return accounts


def read_master_accounts(file_path: str) -> List[Account]:
    """
    Reads and validates the master accounts file.
    Returns a list of Account objects. Errors in format are logged and the line is skipped.
    """
    accounts = []
    try:
        with open(file_path, 'r') as file:
            for line_num, line in enumerate(file, 1):
                clean_line = line.rstrip('\n')
                context = f"Line {line_num}"

                if len(clean_line) != 45:
                    log_constraint_error(f"Invalid length ({len(clean_line)} chars, expected 45)", context)
                    continue

                try:
                    # Extract fields based on fixed-width format
                    account_number_str = clean_line[0:5]
                    name = clean_line[6:26].strip()
                    status = clean_line[27]
                    balance_str = clean_line[29:37]
                    transactions_str = clean_line[38:42]
                    plan_type = clean_line[43:45]

                    # --- Validation ---
                    if not account_number_str.isdigit():
                        log_constraint_error("Account number must be 5 digits", context)
                        continue

                    if not name:
                        log_constraint_error("Account holder name cannot be blank", context)
                        continue

                    if status not in ('A', 'D'):
                        log_constraint_error(f"Invalid status '{status}'. Must be 'A' or 'D'", context)
                        continue

                    if (len(balance_str) != 8 or
                            balance_str[5] != '.' or
                            not balance_str[:5].isdigit() or
                            not balance_str[6:].isdigit()):
                        log_constraint_error(f"Invalid balance format. Expected XXXXX.XX, got {balance_str}", context)
                        continue

                    if balance_str.startswith('-'):
                        log_constraint_error(f"Negative balance detected: {balance_str}", context)
                        continue

                    if not transactions_str.isdigit() or len(transactions_str) != 4:
                        log_constraint_error("Transaction count must be 4 digits", context)
                        continue

                    if plan_type not in ('SP', 'NP'):
                        log_constraint_error(f"Invalid plan type '{plan_type}'. Must be 'SP' or 'NP'", context)
                        continue

                    # --- Conversion ---
                    account_number = int(account_number_str)
                    balance = float(balance_str)
                    transactions = int(transactions_str)

                    # --- Business Rule Validation ---
                    if balance < 0:
                        log_constraint_error("Negative balance is not allowed", context)
                        continue

                    # Create Account object
                    accounts.append(Account(
                        account_number=account_number,
                        name=name,
                        status=status,
                        balance=balance,
                        total_transactions=transactions,
                        plan=plan_type
                    ))

                except (ValueError, IndexError) as e:
                    log_constraint_error(f"Unexpected error parsing line - {str(e)}", context)
                    continue
    except FileNotFoundError:
        log_constraint_error(f"File not found: {file_path}", "File I/O", fatal=True)

    return accounts


def read_daily_transactions(file_path: str) -> List[Transaction]:
    """Read transactions from the daily transactions file."""
    transactions = []
    try:
        with open(file_path, 'r') as file:
            for line_num, line in enumerate(file, 1):
                clean_line = line.rstrip('\n')
                context = f"Line {line_num}"

                if len(clean_line) != 58:
                    log_constraint_error(f"Invalid length ({len(clean_line)} chars, expected 58)", context)
                    continue

                try:
                    code = clean_line[0:2]
                    name = clean_line[3:23].strip()
                    account_number_str = clean_line[24:29]
                    amount_str = clean_line[30:38]
                    misc = clean_line[39:41].strip()

                    # Parse from/to accounts based on transaction type
                    from_acct_str = clean_line[42:47]
                    to_acct_str = clean_line[48:53]

                    # Validation
                    if not account_number_str.isdigit():
                        log_constraint_error("Account number must be 5 digits", context)
                        continue

                    if not from_acct_str.isdigit():
                        log_constraint_error("From account must be 5 digits", context)
                        continue

                    if not to_acct_str.isdigit():
                        log_constraint_error("To account must be 5 digits", context)
                        continue

                    if (len(amount_str) != 8 or
                            amount_str[5] != '.' or
                            not amount_str[:5].isdigit() or
                            not amount_str[6:].isdigit()):
                        log_constraint_error(f"Invalid amount format. Expected XXXXX.XX, got {amount_str}", context)
                        continue

                    account_number = int(account_number_str)
                    amount = float(amount_str)
                    from_acct = int(from_acct_str)
                    to_acct = int(to_acct_str)

                    transactions.append(Transaction(code, float(amount), int(from_acct), int(to_acct), name, account_number, misc))

                except (ValueError, IndexError) as e:
                    log_constraint_error(f"Unexpected error parsing line - {str(e)}", context)
                    continue
    except FileNotFoundError:
        log_constraint_error(f"File not found: {file_path}", "File I/O", fatal=True)

    return transactions


def read_merged_transaction_file(file_path: str) -> List[Transaction]:
    """
    Reads a merged transaction summary file.
    Assumes a format: CODE ACCT_FROM ACCT_TO AMOUNT NAME MISC
    Returns a list of Transaction objects.
    """
    transactions = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if line.strip() == "EOS":
                    continue
                parts = line.strip().split()
                # Basic validation, can be expanded
                if len(parts) < 6:
                    continue

                # Unpack assuming the format
                code, from_acct, to_acct, amount, name, misc = parts[0], parts[1], parts[2], parts[3], parts[4], " ".join(parts[5:])
                transactions.append(Transaction(code, float(amount), int(from_acct), int(to_acct), name, 0, misc))
    except FileNotFoundError:
        log_constraint_error(f"File not found: {file_path}", "File I/O", fatal=True)

    return transactions
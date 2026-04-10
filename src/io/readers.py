"""IO readers for accounts and transactions."""

from typing import List, Optional
from src.models.account import Account
from src.models.transaction import Transaction
from src.backend.utils.print_error import log_constraint_error


def parse_current_account_line(line: str) -> Optional[Account]:
    """Parse one fixed-width current account line, returning None for the end sentinel."""
    line = line.rstrip("\r\n")

    # Check for end-of-file marker before parsing
    if "END_OF_FILE" in line:
        return None

    if len(line) != 37:
        return None

    acct_num = int(line[0:5])
    name = line[6:26].rstrip()
    status = line[27:28]
    balance_str = line[29:37]

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
                clean_line = line.rstrip('\r\n')
                if not clean_line:
                    continue
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
                clean_line = line.rstrip('\r\n')
                if not clean_line:
                    continue
                context = f"Line {line_num}"

                if len(clean_line) != 40:
                    log_constraint_error(f"Invalid length ({len(clean_line)} chars, expected 40)", context)
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
    Reads a merged transaction summary file, where each line is a 40-character fixed-width string.
    Returns a list of Transaction objects.
    """
    transactions = []
    transaction_type_map = {
        '01': 'withdraw', '02': 'transfer', '03': 'paybill',
        '04': 'deposit', '05': 'create', '06': 'delete',
        '07': 'disable', '08': 'changeplan'
    }

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                clean_line = line.rstrip('\r\n')
                context = f"Line {line_num}"

                if not clean_line:
                    continue

                if len(clean_line) not in (40, 46):
                    log_constraint_error(f"Invalid length ({len(clean_line)} chars, expected 40 or 46)", context)
                    continue

                code = clean_line[0:2]
                if code == '00':
                    # End of session marker, skip to next transaction
                    continue

                try:
                    # --- Field Extraction (based on 40-char total length) ---
                    # CC(2)_(1)_Name(20)_(1)_Acct(5)_(1)_Amount(8)_Misc(2) = 40
                    name = clean_line[3:23].strip()
                    account_number_str = clean_line[24:29]
                    amount_str = clean_line[30:38]
                    misc = clean_line[38:40].strip()

                    # --- Validation and Conversion ---
                    transaction_type = transaction_type_map.get(code)
                    if not transaction_type:
                        log_constraint_error(f"Invalid transaction code '{code}'", context)
                        continue

                    if not account_number_str.isdigit():
                        log_constraint_error(f"Account number must be 5 digits, got '{account_number_str}'", context)
                        continue
                    account_number = int(account_number_str)

                    if (len(amount_str) != 8 or amount_str[5] != '.' or
                            not amount_str[:5].isdigit() or not amount_str[6:].isdigit()):
                        log_constraint_error(f"Invalid amount format. Expected XXXXX.XX, got {amount_str}", context)
                        continue
                    amount = float(amount_str)

                    # --- Build Transaction Object ---
                    from_acct = 0
                    to_acct = 0

                    if transaction_type == 'transfer':
                        from_acct = account_number
                        # Attempt to extract the smuggled to_account if present
                        if len(clean_line) == 46:
                            to_acct = int(clean_line[41:46])
                        else:
                            to_acct = 0
                    else:
                        # For other types, the main account is 'account_number'.
                        from_acct = account_number

                    transactions.append(Transaction(
                        transaction_type=transaction_type, amount=amount,
                        from_account=from_acct, to_account=to_acct,
                        name=name, account_number=account_number, misc=misc
                    ))

                except (ValueError, IndexError) as e:
                    log_constraint_error(f"Unexpected error parsing line - {str(e)}", context)
                    continue
    except FileNotFoundError:
        log_constraint_error(f"File not found: {file_path}", "File I/O", fatal=True)
    except Exception as e:
        log_constraint_error(f"Error reading transaction file {file_path}: {e}", "File I/O", fatal=True)

    return transactions
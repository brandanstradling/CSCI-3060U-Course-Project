from src.models.account import Account
from src.models.transaction import Transaction
from src.backend.utils.print_error import log_constraint_error
from typing import List, Dict


def apply_transactions(accounts: List[Account], transactions: List[Transaction]) -> List[Account]:
    """
    Applies a list of transactions to a list of accounts.
    Handles deposits, withdrawals, transfers, and fees.
    Returns the list of updated accounts.
    """
    accounts_by_num: Dict[int, Account] = {acc.account_number: acc for acc in accounts}

    for trans in transactions:
        # Handle create transactions
        if trans.transaction_type == "create":
            if trans.account_number in accounts_by_num:
                log_constraint_error(f"Account {trans.account_number} already exists.", f"Transaction {trans.transaction_type}")
                continue
            # Create new account
            new_account = Account(trans.account_number, trans.amount, trans.name, "A", "SP")  # Default to active, student plan
            accounts_by_num[trans.account_number] = new_account
            continue

        # Handle transfers, which involve two accounts
        if trans.transaction_type == "transfer":
            from_account = accounts_by_num.get(trans.from_account)
            to_account = accounts_by_num.get(trans.to_account)

            if not from_account or not to_account:
                log_constraint_error(f"Invalid account in transfer: {trans.from_account} -> {trans.to_account}", f"Transaction {trans.transaction_type}")
                continue
            
            # Apply transaction to the 'from' account (with fee)
            if from_account.apply_backend_transaction(trans):
                # If successful, apply the amount to the 'to' account (no fee)
                to_account.balance += trans.amount
            else:
                log_constraint_error(f"Failed to process transfer from account {from_account.account_number}.", f"Transaction {trans.transaction_type}")

        # Handle all other transactions that affect a single account
        else:
            # The primary account number should be correctly set in the transaction object
            account = accounts_by_num.get(trans.account_number)
            if not account:
                log_constraint_error(f"Account {trans.account_number} not found for transaction.", f"Transaction {trans.transaction_type}")
                continue

            if not account.apply_backend_transaction(trans):
                # The model method returns False on failure (e.g. insufficient funds, disabled account)
                log_constraint_error(f"Failed to apply {trans.transaction_type} to account {account.account_number}.", f"Transaction {trans.transaction_type}")

    return list(accounts_by_num.values())
"""Shared formatting utilities for fixed-width IO."""


def format_account_number(account_number: int) -> str:
    """Format account number as 5-digit zero-padded string."""
    return str(account_number).zfill(5)


def format_balance(balance: float) -> str:
    """Format balance as XXXXX.XX with 8 characters total."""
    return f"{balance:08.2f}"


def format_transaction_count(count: int) -> str:
    """Format transaction count as 4-digit zero-padded string."""
    return str(count).zfill(4)


def format_name(name: str, width: int = 20) -> str:
    """Format name left-justified with spaces to specified width."""
    return name.ljust(width)


def parse_balance(balance_str: str) -> float:
    """Parse balance from XXXXX.XX format."""
    if (len(balance_str) != 8 or
            balance_str[5] != '.' or
            not balance_str[:5].isdigit() or
            not balance_str[6:].isdigit()):
        raise ValueError(f"Invalid balance format: {balance_str}")
    return float(balance_str)
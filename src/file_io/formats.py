"""Helpers for fixed-width string formatting."""

NAME_W = 20
ACCT_W = 5
AMT_W = 8
MISC_W = 2
LINE_W = 40


def left(text: str, width: int) -> str:
    """Left-justify text and pad with spaces to a fixed width."""
    return (text or "")[:width].ljust(width, " ")


def zfill_int(n: int, width: int) -> str:
    """Zero-fill an integer to a fixed width."""
    return str(int(n)).zfill(width)[-width:]


def money(amount: float, width: int) -> str:
    """Format a float as money with two decimals and zero-fill to a fixed width."""
    s = f"{amount:.2f}"
    return s.zfill(width)[-width:]

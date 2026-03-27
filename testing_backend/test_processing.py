from src.backend.processing import apply_transactions
from src.models.account import Account
from src.models.transaction import Transaction

def test_apply_transactions_deposit():
    acc = Account(1, 100.0, "Test", "A", "SP")
    t = Transaction("deposit", 50.0, 0, 0, "Test", 1)

    result = apply_transactions([acc], [t])

    assert result[0].balance > 100.0


def test_apply_transactions_withdraw_success():
    acc = Account(1, 200.0, "Test", "A", "SP")
    t = Transaction("withdraw", 50.0, 0, 0, "Test", 1)

    result = apply_transactions([acc], [t])

    assert result[0].balance < 200.0


def test_apply_transactions_withdraw_fail():
    acc = Account(1, 10.0, "Test", "A", "SP")
    t = Transaction("withdraw", 50.0, 0, 0, "Test", 1)

    result = apply_transactions([acc], [t])

    assert result[0].balance == 10.0  # unchanged


def test_transfer_success():
    acc1 = Account(1, 200.0, "A", "A", "SP")
    acc2 = Account(2, 100.0, "B", "A", "SP")

    t = Transaction("transfer", 50.0, 1, 2, "A", 1)

    result = apply_transactions([acc1, acc2], [t])

    # money moved
    assert any(a.balance > 100.0 for a in result)
    assert any(a.balance < 200.0 for a in result)


def test_transfer_invalid_account():
    acc1 = Account(1, 200.0, "A", "A", "SP")

    t = Transaction("transfer", 50.0, 1, 99, "A", 1)

    result = apply_transactions([acc1], [t])

    # no crash, balance unchanged
    assert result[0].balance == 200.0


def test_account_not_found():
    acc = Account(1, 100.0, "A", "A", "SP")

    t = Transaction("deposit", 50.0, 0, 0, "A", 999)

    result = apply_transactions([acc], [t])

    assert result[0].balance == 100.0


def test_disabled_account():
    acc = Account(1, 100.0, "A", "D", "SP")

    t = Transaction("deposit", 50.0, 0, 0, "A", 1)

    result = apply_transactions([acc], [t])

    assert result[0].balance == 100.0


def test_multiple_transactions_loop():
    acc = Account(1, 100.0, "A", "A", "SP")

    transactions = [
        Transaction("deposit", 50.0, 0, 0, "A", 1),
        Transaction("withdraw", 20.0, 0, 0, "A", 1),
        Transaction("withdraw", 500.0, 0, 0, "A", 1),  # fail
    ]

    result = apply_transactions([acc], transactions)

    assert result[0].balance != 100.0
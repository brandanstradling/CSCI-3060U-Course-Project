from src.backend.utils.print_error import log_constraint_error

def test_non_fatal_error(capsys):
    log_constraint_error("Something went wrong", "Transaction deposit", fatal=False)
    captured = capsys.readouterr()
    assert "ERROR: Transaction deposit: Something went wrong" in captured.out

def test_fatal_error(capsys):
    log_constraint_error("File missing", "accounts.txt", fatal=True)
    captured = capsys.readouterr()
    assert "ERROR: Fatal error - File accounts.txt - File missing" in captured.out
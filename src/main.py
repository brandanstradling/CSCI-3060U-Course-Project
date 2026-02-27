"""Program entry point that starts the interactive front end."""

import sys
from controller import FrontEndApp

def main() -> None:
    test_name = sys.argv[1] if len(sys.argv) > 1 else "test1"
    current_accounts_path = sys.argv[2] if len(sys.argv) > 2 else "data/current_accounts.txt"
    daily_transactions_path = f"out/actual/{test_name}.atf"
    app = FrontEndApp(
        current_accounts_path=current_accounts_path,
        daily_transactions_path=daily_transactions_path,
    )
    app.run()

if __name__ == "__main__":
    main()

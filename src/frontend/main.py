"""Program entry point that starts the interactive front end."""

import sys
import os
import argparse

# Add the project root to Python path for imports
project_root = os.path.join(os.path.dirname(__file__), '..', '..')
sys.path.insert(0, os.path.abspath(project_root))

from src.frontend.controller import FrontEndApp

def main() -> None:
    parser = argparse.ArgumentParser(description="Bank Frontend")
    parser.add_argument("current_accounts_path", nargs='?', default="data/current_accounts.txt", help="Current accounts file")
    parser.add_argument("daily_transactions_path", nargs='?', default="data/daily_transactions.txt", help="Daily transactions file")
    args = parser.parse_args()

    # Interactive mode
    app = FrontEndApp(
        current_accounts_path=args.current_accounts_path,
        daily_transactions_path=args.daily_transactions_path,
    )
    app.run()

if __name__ == "__main__":
    main()

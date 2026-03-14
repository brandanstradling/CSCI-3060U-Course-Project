"""Program entry point that starts the interactive front end."""

import sys
import os

# Add the project root to Python path for imports
project_root = os.path.join(os.path.dirname(__file__), '..', '..')
sys.path.insert(0, os.path.abspath(project_root))

from src.frontend.controller import FrontEndApp

def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="Bank Frontend")
    parser.add_argument("--test", nargs='?', const="test1", help="Run test mode with given test name")
    parser.add_argument("test_name", nargs='?', default="test1", help="Test name for input file")
    parser.add_argument("current_accounts_path", nargs='?', default="data/current_accounts.txt", help="Current accounts file")
    args = parser.parse_args()

    if args.test:
        # Run in test mode: simulate input from input/testX.txt
        test_file = f"input/{args.test}.txt"
        if os.path.exists(test_file):
            print(f"Running test {args.test}...")
            # Read the test file and simulate input
            with open(test_file, 'r') as f:
                test_commands = f.read().splitlines()
            
            # Mock input to read from test_commands
            import builtins
            original_input = builtins.input
            builtins.input = lambda: test_commands.pop(0) if test_commands else "logout"
            
            try:
                current_accounts_path = args.current_accounts_path
                daily_transactions_path = f"data/{args.test}_transactions.atf"
                app = FrontEndApp(
                    current_accounts_path=current_accounts_path,
                    daily_transactions_path=daily_transactions_path,
                )
                app.run()
            finally:
                builtins.input = original_input
            print(f"Test {args.test} completed.")
        else:
            print(f"Test file {test_file} not found.")
    else:
        # Interactive mode
        test_name = args.test_name
        current_accounts_path = args.current_accounts_path
        daily_transactions_path = f"out/actual/{test_name}.atf"
        app = FrontEndApp(
            current_accounts_path=current_accounts_path,
            daily_transactions_path=daily_transactions_path,
        )
        app.run()

if __name__ == "__main__":
    main()

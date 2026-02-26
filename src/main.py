"""Program entry point that starts the interactive front end."""

import sys
from controller import FrontEndApp


def main() -> None:
    """Create the app and start the input loop."""
    app = FrontEndApp(
        current_accounts_path = sys.argv[1] if len(sys.argv) > 1 else "data/current_accounts.txt",
        daily_transactions_path = sys.argv[2] if len(sys.argv) > 2 else "out/daily_transactions.txt",
    )
    app.run()


if __name__ == "__main__":
    main()

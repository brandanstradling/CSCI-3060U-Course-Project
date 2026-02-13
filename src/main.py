"""Program entry point that starts the interactive front end."""

from controller import FrontEndApp


def main() -> None:
    """Create the app and start the input loop."""
    app = FrontEndApp(
        current_accounts_path="data/current_accounts.txt",
        daily_transactions_path="out/daily_transactions.txt",
    )
    app.run()


if __name__ == "__main__":
    main()

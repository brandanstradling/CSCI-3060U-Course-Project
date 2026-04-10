"""
Main executable for the backend system.

This script orchestrates the batch processing of transactions. It reads the
master accounts file and a merged transaction summary file, applies the
transactions to the accounts, and writes the new master accounts file and
the new current accounts file.

Usage:
    python -m src.backend.main <master_accounts_file> <transaction_summary_file> <new_master_accounts_file> <new_current_accounts_file>
"""

import argparse
import sys
import os

# Add the project root to Python path for imports
project_root = os.path.join(os.path.dirname(__file__), '..', '..')
sys.path.insert(0, os.path.abspath(project_root))

from src.io.readers import read_master_accounts, read_merged_transaction_file
from src.io.writers import write_master_accounts_file, write_current_accounts_file
from src.backend.processing import apply_transactions


def main():
    """Main backend processing function."""
    parser = argparse.ArgumentParser(description="Bank Backend Processing")
    parser.add_argument("master_accounts_file", help="Input master accounts file")
    parser.add_argument("transaction_summary_file", help="Input merged transaction summary file")
    parser.add_argument("new_master_accounts_file", help="Output new master accounts file")
    parser.add_argument("new_current_accounts_file", help="Output new current accounts file")
    args = parser.parse_args()

    # Check if input files exist
    if not os.path.exists(args.master_accounts_file):
        print(f"Error: Master accounts file '{args.master_accounts_file}' not found.")
        return
    if not os.path.exists(args.transaction_summary_file):
        print(f"Error: Transaction summary file '{args.transaction_summary_file}' not found.")
        return

    # 1. Read initial data
    accounts = read_master_accounts(args.master_accounts_file)
    transactions = read_merged_transaction_file(args.transaction_summary_file)

    # 2. Process transactions
    updated_accounts = apply_transactions(accounts, transactions)

    # 3. Write output files
    write_master_accounts_file(updated_accounts, args.new_master_accounts_file)
    write_current_accounts_file(updated_accounts, args.new_current_accounts_file)

    print("Backend processing complete.")

if __name__ == "__main__":
    main()
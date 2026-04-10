"""Test utilities for frontend testing."""

import os
import sys

# Add the project root to Python path for imports
project_root = os.path.join(os.path.dirname(__file__), '..', '..')
sys.path.insert(0, os.path.abspath(project_root))

from src.frontend.controller import FrontEndApp

def run_test_mode(test_name: str, current_accounts_path: str, test_file_path: str = None, transactions_path: str = None, quiet: bool = False) -> None:
    """Run the frontend in test mode with simulated input."""
    if test_file_path is None:
        test_file_path = f"operation_scripts/input/{test_name}.txt"
    if transactions_path is None:
        transactions_path = f"data/{test_name}_transactions.atf"
    
    if not os.path.exists(test_file_path):
        if not quiet:
            print(f"Test file {test_file_path} not found.")
        return
    
    if not quiet:
        print(f"Running test {test_name}...")
    
    # Read test commands
    with open(test_file_path, 'r') as f:
        test_commands = f.read().splitlines()
    
    # Mock input
    import builtins
    original_input = builtins.input
    builtins.input = lambda: test_commands.pop(0) if test_commands else "logout"
    
    try:
        app = FrontEndApp(
            current_accounts_path=current_accounts_path,
            daily_transactions_path=transactions_path,
        )
        app.run()
    finally:
        builtins.input = original_input
    
    if not quiet:
        print(f"Test {test_name} completed.")
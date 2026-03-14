"""Configuration constants for the banking system."""

# Transaction fees by account plan
TRANSACTION_FEES = {
    'NP': 0.10,  # Non-Prime
    'SP': 0.05,  # Student Plan
}

# Paybill companies
PAYBILL_COMPANIES = {"EC", "CQ", "FI"}

# Fixed time string for transactions (frontend)
FIXED_TIME_STR = "2025-03-01 10:00:00"

# Session limits
WITHDRAWAL_LIMIT = 500.00
TRANSFER_LIMIT = 1000.00  # Assuming, need to check
PAYBILL_LIMIT = 2000.00   # Assuming
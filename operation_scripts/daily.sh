#!/bin/bash
# daily.sh - Script to simulate a single day of banking transactions

if [ "$#" -lt 5 ]; then
    echo "Usage: $0 <master_accounts_in> <current_accounts_in> <master_accounts_out> <current_accounts_out> <session_name_1> [session_name_2 ...]"
    exit 1
fi

MASTER_IN=$1
CURRENT_IN=$2
MASTER_OUT=$3
CURRENT_OUT=$4
shift 4
SESSIONS=$@

MERGED_TX_FILE="$(pwd)/operation_scripts/output/merged_daily_transactions.atf"
> "$MERGED_TX_FILE" # Clear the merged file for the new day

echo "--- Starting Daily Runs ---"
for SESSION in $SESSIONS; do
    echo "Running Front End for session: $SESSION"
    if ! python3 -c "from src.frontend.test_utils import run_test_mode; run_test_mode('$SESSION', '$CURRENT_IN', transactions_path='operation_scripts/output/${SESSION}_transactions.atf')" ; then
        echo "ERROR: Frontend failed for session $SESSION"
        exit 1
    fi
    
    SESSION_TX_FILE="$(pwd)/operation_scripts/output/${SESSION}_transactions.atf"
    if [ -f "$SESSION_TX_FILE" ]; then
        echo "Merging transactions from $SESSION_TX_FILE"
        cat "$SESSION_TX_FILE" >> "$MERGED_TX_FILE"
    else
        echo "WARNING: Transaction file not found for session $SESSION"
    fi
done

echo "Running Back End..."
if ! python3 -m src.backend.main "$MASTER_IN" "$MERGED_TX_FILE" "$MASTER_OUT" "$CURRENT_OUT" ; then
    echo "ERROR: Backend processing failed"
    exit 1
fi
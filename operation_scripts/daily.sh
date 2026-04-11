#!/bin/bash
# daily.sh - Script to process a single day of banking transactions

# Check if sufficient arguments are provided
if [ "$#" -lt 5 ]; then
    echo "Usage: $0 <day> <master_in> <current_in> <master_out> <current_out> [sessions...]"
    exit 1
fi

DAY=$1
MASTER_IN=$2
CURRENT_IN=$3
MASTER_OUT=$4
CURRENT_OUT=$5
shift 5
SESSIONS="$@"

mkdir -p operation_scripts/output

MERGED_TX_FILE="operation_scripts/output/merged_transactions_day${DAY}.txt"
> "$MERGED_TX_FILE" # Create or truncate the merged transactions file

# (i) Run Front End for each session and (ii) concatenate into merged file
for session in $SESSIONS; do
    SESSION_INPUT="operation_scripts/input/${session}.txt"
    SESSION_OUTPUT="operation_scripts/output/${session}_transaction.txt"
    
    if [ -f "$SESSION_INPUT" ]; then
        echo "  Running frontend for session: $session"
        python -m src.frontend.main "$CURRENT_IN" "$SESSION_OUTPUT" < "$SESSION_INPUT"
        
        # Remove trailing 00 from each session to avoid multiple markers in merged file.
        sed '$d' "$SESSION_OUTPUT" >> "$MERGED_TX_FILE"
    else
        echo "  Warning: Input file $SESSION_INPUT not found. Skipping session."
    fi
done

# Append the required empty session (00 transaction code) to mark end of batch.
# Needs to match exactly the fixed-length 40 char format, filling unused numeric fields with zeros.
echo "00                      00000 00000.00  " >> "$MERGED_TX_FILE"

# (iii) Run Back End with the merged transaction file
echo "  Running backend for day: $DAY"
python -m src.backend.main "$MASTER_IN" "$MERGED_TX_FILE" "$MASTER_OUT" "$CURRENT_OUT"

# Ensure END_OF_FILE is correctly formatted (Back End might output legacy ENDOFFILE)
if grep -q "ENDOFFILE" "$CURRENT_OUT"; then
    sed 's/ENDOFFILE  /END_OF_FILE/g' "$CURRENT_OUT" > "${CURRENT_OUT}.tmp" && mv "${CURRENT_OUT}.tmp" "$CURRENT_OUT"
fi
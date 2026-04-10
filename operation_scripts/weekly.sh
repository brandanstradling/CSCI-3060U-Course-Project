#!/bin/bash
# weekly.sh - Script to simulate 7 days of banking transactions

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

chmod +x operation_scripts/daily.sh
chmod +x operation_scripts/verify_balances.sh

# Reset the base starting files to ensure a clean slate for the weekly simulation
mkdir -p data
> data/master_accounts_day0.txt
echo "00000 END_OF_FILE         A 00000.00" > data/current_accounts_day0.txt

mkdir -p operation_scripts/output

# Define the names of your test files for each day.
# These require corresponding files in your input/ directory (e.g., input/day1_session1.txt)
DAY1_SESSIONS="day1_session1 day1_session2"
DAY2_SESSIONS="day2_session1"
DAY3_SESSIONS="day3_session1 day3_session2"
DAY4_SESSIONS="day4_session1"
DAY5_SESSIONS="day5_session1 day5_session2"
DAY6_SESSIONS="day6_session1"
DAY7_SESSIONS="day7_session1 day7_session2"

for day in {1..7}; do
    echo "============================================="
    echo "                 DAY $day                    "
    echo "============================================="
    
    if [ $day -eq 1 ]; then
        MASTER_IN="data/master_accounts_day0.txt"
        CURRENT_IN="data/current_accounts_day0.txt"
    else
        MASTER_IN="operation_scripts/output/master_accounts_day$((day-1)).txt"
        CURRENT_IN="operation_scripts/output/current_accounts_day$((day-1)).txt"
    fi
    MASTER_OUT="operation_scripts/output/master_accounts_day${day}.txt"
    CURRENT_OUT="operation_scripts/output/current_accounts_day${day}.txt"
    
    var_name="DAY${day}_SESSIONS"
    SESSIONS=${!var_name}
    
    echo "Running daily script for day $day..."
    if ! ./operation_scripts/daily.sh "$day" "$MASTER_IN" "$CURRENT_IN" "$MASTER_OUT" "$CURRENT_OUT" $SESSIONS ; then
        echo "ERROR: Daily script failed for day $day"
        exit 1
    fi
done

echo "Weekly simulation complete."

# Run the automated assertions
./operation_scripts/verify_balances.sh

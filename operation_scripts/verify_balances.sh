#!/bin/bash
# verify_balances.sh - Automated tests for End-of-Week system state

DAY7_CURRENT_FILE="operation_scripts/output/current_accounts_day7.txt"
DAY7_MASTER_FILE="operation_scripts/output/master_accounts_day7.txt"
DAY6_MASTER_FILE="operation_scripts/output/master_accounts_day6.txt"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "============================================="
echo "        RUNNING AUTOMATED ASSERTIONS         "
echo "============================================="

if [ ! -f "$DAY7_CURRENT_FILE" ] || [ ! -f "$DAY7_MASTER_FILE" ]; then
    echo -e "${RED}❌ ERROR: Final Day 7 output files not found!${NC}"
    exit 1
fi

FAILURES=0

# Assert Current Account (Balance and Status)
assert_current_account() {
    local account_num=$1
    local expected_balance=$2
    local expected_status=$3
    
    local formatted_balance=$(printf "%08.2f" "$expected_balance")
    
    local account_line=$(grep "^${account_num}" "$DAY7_CURRENT_FILE")
    
    if [ -z "$account_line" ]; then
        echo -e "${RED}❌ FAIL: [Current] Account $account_num not found!${NC}"
        FAILURES=$((FAILURES + 1))
        return 1
    fi
    
    local actual_status=$(echo "$account_line" | cut -c28)
    
    if [[ "$account_line" == *"$formatted_balance"* ]] && [ "$actual_status" == "$expected_status" ]; then
        echo -e "${GREEN}✅ PASS: [Current] Account $account_num matches balance ($formatted_balance) & status ($expected_status).${NC}"
    else
        echo -e "${RED}❌ FAIL: [Current] Account $account_num data mismatch!${NC}"
        echo "   Expected: Balance *$formatted_balance*, Status '$expected_status'"
        echo "   Actual:   $account_line"
        FAILURES=$((FAILURES + 1))
    fi
}

# Assert Master Account (Balance, Status, TX Count, and Plan)
assert_master_account() {
    local account_num=$1
    local expected_balance=$2
    local expected_status=$3
    local expected_tx=$4
    local expected_plan=$5
    local target_file=${6:-$DAY7_MASTER_FILE}
    
    local formatted_balance=$(printf "%08.2f" "$expected_balance")
    local formatted_tx=$(printf "%04d" "$expected_tx")
    local account_line=$(grep "^${account_num} " "$target_file")
    
    if [ -z "$account_line" ]; then
        echo -e "${RED}❌ FAIL: [Master] Account $account_num not found in $(basename "$target_file")!${NC}"
        FAILURES=$((FAILURES + 1))
        return 1
    fi
    
    local actual_status=$(echo "$account_line" | cut -c28)
    local actual_tx=$(echo "$account_line" | cut -c39-42)
    local actual_plan=$(echo "$account_line" | cut -c44-45)
    
    if [[ "$account_line" == *"$formatted_balance"* ]] && [ "$actual_status" == "$expected_status" ] && [ "$actual_tx" == "$formatted_tx" ] && [ "$actual_plan" == "$expected_plan" ]; then
        echo -e "${GREEN}✅ PASS: [Master] Account $account_num matches balance ($formatted_balance), status ($expected_status), TXs ($formatted_tx), & plan ($expected_plan).${NC}"
    else
        echo -e "${RED}❌ FAIL: [Master] Account $account_num data mismatch!${NC}"
        echo "   Expected: Balance *$formatted_balance*, Status '$expected_status', TXs '$formatted_tx', Plan '$expected_plan'"
        echo "   Actual:   $account_line"
        FAILURES=$((FAILURES + 1))
    fi
}

# Assert Account is Deleted
assert_deleted() {
    local account_num=$1
    
    local current_line=$(grep "^${account_num}" "$DAY7_CURRENT_FILE")
    local master_line=$(grep "^${account_num} " "$DAY7_MASTER_FILE")
    
    if [ -z "$current_line" ] && [ -z "$master_line" ]; then
        echo -e "${GREEN}✅ PASS: Account $account_num was properly deleted from all files.${NC}"
    else
        echo -e "${RED}❌ FAIL: Account $account_num was NOT completely deleted!${NC}"
        [ -n "$current_line" ] && echo "   Found in Current: $current_line"
        [ -n "$master_line" ] && echo "   Found in Master:  $master_line"
        FAILURES=$((FAILURES + 1))
    fi
}

# Assert ENDOFFILE marker
assert_eof_marker() {
    local last_line=$(tail -n 1 "$DAY7_CURRENT_FILE")
    if [[ "$last_line" == *"END_OF_FILE"* ]]; then
        echo -e "${GREEN}✅ PASS: [Current] END_OF_FILE marker is present at the end of the file.${NC}"
    else
        echo -e "${RED}❌ FAIL: [Current] END_OF_FILE marker missing or not at the end!${NC}"
        FAILURES=$((FAILURES + 1))
    fi
}

# ---------------------------------------------------------
# TEST SUITE
# ---------------------------------------------------------
# Note: Adjust balances based on exact transaction fees configured in src/config.py

# Alice (Created Day 1 -> Active)
assert_current_account "10001" 529.95 "A"
assert_master_account  "10001" 529.95 "A" 1 "SP"

# Bob (Created Day 1 -> Disabled Day 6 -> Deleted Day 7)
# Assert Bob was successfully disabled on Day 6 with correct state before deletion
assert_master_account "10002" 314.90 "D" 2 "SP" "$DAY6_MASTER_FILE"
# Assert Bob is gone by Day 7
assert_deleted "10002"

# Charlie (Created Day 4 -> Active)
assert_current_account "10003" 799.95 "A"
assert_master_account  "10003" 799.95 "A" 1 "SP"

# System State
assert_eof_marker

echo "============================================="
if [ $FAILURES -eq 0 ]; then
    echo -e "${GREEN}🎉 ALL TESTS PASSED!${NC}"
    exit 0
else
    echo -e "${RED}⚠️  $FAILURES TEST(S) FAILED.${NC}"
    exit 1
fi
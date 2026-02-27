#!/bin/bash

echo "Running all tests..."

for file in input/*.txt; do

    test_name=$(basename "$file" .txt)

    echo "Running test: $testname"

    python src/main.py < "$file" > "out/$testname.out"

    cp data/daily_transactions.txt out/$testname.atf

    echo "-----------------------------"
done

echo "All tests completed."
#!/bin/bash

mkdir -p out/actual

echo "Running all tests..."

for file in input/*.txt; do
    test_name=$(basename "$file" .txt)
    echo "Running test: $test_name"

    # Pass test_name so main writes out/actual/test_name.atf
    # Keep stderr in a separate .err file (NOT .atf)
    python src/main.py "$test_name" data/current_accounts.txt \
        < "$file" \
        > "out/actual/$test_name.out" \
        2> "out/actual/$test_name.err"

    echo "-----------------------------"
done

echo "All tests completed."
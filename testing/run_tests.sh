#!/bin/bash

if [ ! -d "src" ] || [ ! -d "input" ] || [ ! -f "data/current_accounts.txt" ]; then
    echo "Error: Must run from project root directory"
    echo "Current directory: $(pwd)"
    exit 1
fi

mkdir -p out/actual

echo "Running all tests..."
echo "========================================"

test_count=0
success_count=0

for file in input/test*.txt; do
    if [ ! -f "$file" ]; then
        echo "Error: Input file not found: $file"
        continue
    fi
    
    test_name=$(basename "$file" .txt)
    echo -n "Running test: $test_name ... "
    ((test_count++))

    if python3 src/main.py "$test_name" data/current_accounts.txt \
        < "$file" \
        > "out/actual/$test_name.out" \
        2> "out/actual/$test_name.err"; then
        echo "OK"
        ((success_count++))
    else
        echo "FAILED (Python error)"
    fi
done

echo "========================================"
echo "Completed: $success_count/$test_count tests ran successfully"

if [ $success_count -eq $test_count ] && [ $test_count -gt 0 ]; then
    echo "Ready to run check_tests.sh to validate outputs."
    exit 0
else
    echo "Some tests failed."
    exit 1
fi
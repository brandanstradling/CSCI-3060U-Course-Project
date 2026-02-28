#!/bin/bash

# Ensure output directories exist
mkdir -p out/actual
mkdir -p out/expected

echo "Running all tests..."

for file in input/*.txt; do
    test_name=$(basename "$file" .txt)
    echo "Running test: $test_name"

    # Redirect transaction output to .atf and terminal output to .out
    python src/main.py < "$file" > out/actual/"$test_name".out 2> out/actual/"$test_name".atf

    echo "-----------------------------"
done

echo "All tests completed."

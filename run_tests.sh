#!/bin/bash

# Ensure output directories exist
mkdir -p out/actual
mkdir -p out/expected

echo "Running all tests..."

for file in input/*.txt; do
    test_name=$(basename "$file" .txt)
    echo "Running test: $test_name"

    # Redirect input file to Python script and capture output
    python src/main.py < "$file" > out/actual/"$test_name".out 2> /dev/null

    echo "-----------------------------"
done

echo "All tests completed."

#!/bin/bash

echo "Validating test results..."

# Ensure expected directories exist
mkdir -p out/expected

for file in input/*.txt; do
    testname=$(basename "$file" .txt)
    echo "Checking test: $testname"

    # Compare transaction files (ATF vs ETF)
    echo "Comparing transaction files..."
    diff out/actual/"$testname".atf out/expected/"$testname".etf

    if [ $? -eq 0 ]; then
        echo "Transaction file matches."
    else
        echo "Transaction file DOES NOT match!"
    fi

    # Compare terminal output (OUT vs OUT)
    echo "Comparing terminal output..."
    diff out/actual/"$testname".out out/expected/"$testname".out

    if [ $? -eq 0 ]; then
        echo "Terminal output matches."
    else
        echo "Terminal output DOES NOT match!"
    fi

    echo "-----------------------------"
done

echo "Validation completed."

#!/bin/bash

echo "Validating test results..."

for file in input/*.txt; do

    testname=$(basename "$file" .txt)

    echo "Checking test: $testname"

    echo "Comparing transaction files..."
    diff out/$testname.atf out/expected/$testname.etf

    if [ $? -eq 0 ]; then
        echo "Transaction file matches."
    else
        echo "Transaction file DOES NOT match!"
    fi

    echo "Comparing terminal output..."
    diff out/$testname.out out/expected/$testname.eout

    if [ $? -eq 0 ]; then
        echo "Terminal output matches."
    else
        echo "Terminal output DOES NOT match!"
    fi

    echo "-----------------------------"
done

echo "Validation completed."
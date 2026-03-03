#!/bin/bash

if [ ! -d "src" ] || [ ! -d "out" ]; then
    echo "Error: Must run from project root directory"
    echo "Current directory: $(pwd)"
    exit 1
fi

echo "Validating test results..."
echo "========================================"

mkdir -p out/expected

test_count=0
passed_count=0

for file in input/test*.txt; do
    if [ ! -f "$file" ]; then
        continue
    fi
    
    testname=$(basename "$file" .txt)
    ((test_count++))
    
    if [ ! -f "out/actual/$testname.atf" ] || [ ! -f "out/actual/$testname.out" ]; then
        echo "❌ $testname - Missing output files (run run_tests.sh first)"
        continue
    fi
    
    if [ ! -f "out/expected/$testname.etf" ] || [ ! -f "out/expected/$testname.out" ]; then
        echo "❌ $testname - Missing expected files"
        continue
    fi
    
    # Compare transaction files (suppress diff output, just check result)
    diff -q out/actual/"$testname".atf out/expected/"$testname".etf > /dev/null 2>&1
    atf_match=$?
    
    # Compare terminal output
    diff -q out/actual/"$testname".out out/expected/"$testname".out > /dev/null 2>&1
    out_match=$?
    
    if [ $atf_match -eq 0 ] && [ $out_match -eq 0 ]; then
        echo "✓ $testname - Transaction file matches, Terminal output matches"
        ((passed_count++))
    elif [ $atf_match -eq 0 ]; then
        echo "⚠ $testname - Transaction OK, Terminal output DIFFERS"
    elif [ $out_match -eq 0 ]; then
        echo "⚠ $testname - Terminal OK, Transaction file DIFFERS"
    else
        echo "❌ $testname - Transaction file DIFFERS, Terminal output DIFFERS"
    fi
done

echo "========================================"
echo "Results: $passed_count/$test_count tests passed"

if [ $passed_count -eq $test_count ] && [ $test_count -gt 0 ]; then
    echo "✓ All tests passed!"
    exit 0
else
    echo "✗ Some tests failed or missing outputs."
    exit 1
fi

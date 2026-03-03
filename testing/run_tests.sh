#!/bin/bash

if command -v python3 >/dev/null 2>&1; then
    PYTHON=python3
elif command -v python >/dev/null 2>&1; then
    PYTHON=python
else
    echo "Error: python3 or python not found" >&2
    exit 1
fi

mkdir -p out/actual

failed=0
for file in input/test*.txt; do
    [ -f "$file" ] || continue
    testname=$(basename "$file" .txt)
    echo "Running $testname"
    if "$PYTHON" src/main.py "$testname" data/current_accounts.txt \
        < "$file" \
        > "out/actual/$testname.out" \
        2> "out/actual/$testname.err"; then
        echo "OK"
    else
        echo "FAILED $testname"
        failed=1
    fi
done

exit $failed
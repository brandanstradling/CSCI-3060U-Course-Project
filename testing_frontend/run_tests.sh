#!/bin/bash

if command -v python3 >/dev/null 2>&1; then
    PYTHON=python3
elif command -v python >/dev/null 2>&1; then
    PYTHON=python
else
    echo "Error: python3 or python not found" >&2
    exit 1
fi

cd ..
mkdir -p testing_frontend/out/actual

failed=0
for file in testing_frontend/input/test*.txt; do
    [ -f "$file" ] || continue
    testname=$(basename "$file" .txt)
    echo "Running $testname"
    if "$PYTHON" -c "
from src.frontend.test_utils import run_test_mode
run_test_mode('$testname', 'data/current_accounts.txt', '$file', 'testing_frontend/out/actual/$testname.atf', quiet=True)
" > "testing_frontend/out/actual/$testname.out" 2> "testing_frontend/out/actual/$testname.err"; then
        echo "OK"
    else
        echo "FAILED $testname"
        failed=1
    fi
done

exit $failed
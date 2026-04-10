#!/bin/bash

cd ..
ok=0
total=0
for file in testing_frontend/input/test*.txt; do
    [ -f "$file" ] || continue
    testname=$(basename "$file" .txt)
    total=$((total+1))

    if [ ! -f "testing_frontend/out/actual/$testname.atf" ] || [ ! -f "testing_frontend/out/actual/$testname.out" ]; then
        echo "$testname: MISSING actual outputs"
        continue
    fi
    if [ ! -f "testing_frontend/out/expected/$testname.etf" ] || [ ! -f "testing_frontend/out/expected/$testname.out" ]; then
        echo "$testname: MISSING expected outputs"
        continue
    fi

    diff -q "testing_frontend/out/actual/$testname.atf" "testing_frontend/out/expected/$testname.etf" >/dev/null 2>&1
    atf=$?
    diff -q "testing_frontend/out/actual/$testname.out" "testing_frontend/out/expected/$testname.out" >/dev/null 2>&1
    out=$?

    if [ $atf -eq 0 ] && [ $out -eq 0 ]; then
        echo "$testname: PASS"
        ok=$((ok+1))
    else
        echo "$testname: FAIL"
    fi
done

echo "$ok/$total passed"
if [ $ok -ne $total ]; then
    exit 1
fi
exit 0

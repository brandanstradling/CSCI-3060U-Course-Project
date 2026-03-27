# CSCI 3060U - Phase 5 Back End Unit Testing Report

## Phase 5 Coverage Summary

- `Account.apply_backend_transaction()`:
  - Coverage target: statement coverage
  - Contains decisions for status, transaction_type (`withdraw`, `deposit`, `transfer`, `changeplan`)
- `apply_transactions()`:
  - Coverage target: decision and loop coverage
  - Contains loop over transactions and decisions for transfer vs non-transfer, account existence, transfer validity

## Test Cases and Coverage Mapping

| Test Name | Method | Coverage Focus | Case Covered |
|-----------|--------|----------------|--------------|
| test_apply_transactions_deposit | apply_transactions + apply_backend_transaction | statement/conditional | deposit path success, fee applied logic |
| test_apply_transactions_withdraw_success | apply_transactions + apply_backend_transaction | statement/conditional | withdraw path success with sufficient funds |
| test_apply_transactions_withdraw_fail | apply_transactions + apply_backend_transaction | statement/conditional | withdraw path fail, insufficient funds |
| test_transfer_success | apply_transactions | decision/loop+transfer-success | both accounts present and updated, includes transfer path and nested branch |
| test_transfer_invalid_account | apply_transactions | decision/loop+transfer-failure | invalid transfer account path with constraint error |
| test_account_not_found | apply_transactions | decision/loop+account-missing | account lookup fail path |
| test_disabled_account | apply_transactions + apply_backend_transaction | decision/loop+status-disabled | disabled status prevents operations |
| test_multiple_transactions_loop | apply_transactions | loop coverage | multi-transaction sequence with success+failure path |

## Test Run Results

- Command executed: `python -m pytest -q`
- Result: `10 passed`
- No current failures uncovered in this implementation run.

## Failure Log (Phase 5)

| Test Name | What Was Tested | Nature of Failure (if any) | Error in Code | Fix Applied |
|-----------|-----------------|---------------------------|---------------|-------------|
| (none) | backend transaction processing | no failures found in this run | n/a | n/a |

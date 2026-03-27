# CSCI 3060U - Phase 3 Failure Log

## Test Failures

| Test Name | What Was Tested | Nature of Failure | Error in Code | Fix Applied |
|-----------|-----------------|-------------------|---------------|-------------|
| test1 | Admin changeplan transaction | Only login transaction recorded; changeplan not logged | Input file did not match controller’s prompt structure; login was being written to transaction log | Corrected input format and filtered login/logout from transaction writer |
| test2 | Admin create transaction | Create transaction not recorded; login only written | Parameters for create not provided on separate input lines | Updated test input to match command + parameter sequence |
| test3 | Admin delete transaction | Delete not logged; invalid transaction printed | Delete command parameters not aligned with expected prompts | Rewrote test input file to follow controller prompt order |
| test4 | Standard login/logout | No .atf file created | Missing required account number/password lines caused EOF before logout | Added all required login inputs and ensured logout executed |
| test5 | Standard paybill transaction | Invalid number and invalid transaction errors | Account number expected as integer but incorrect format supplied | Corrected input file to provide numeric account number and separate lines for company and amount |
| test6 | Standard transfer transaction | Transfer not logged; login only recorded | Transfer parameters not supplied in correct order | Updated input file to match controller’s prompt sequence |
| test7 | Balance command | Balance not executed; invalid transaction printed | Command keyword or input structure mismatch | Standardized command usage and corrected test input structure |
| test8 | Standard deposit transaction | Deposit not recorded; invalid transaction shown | Deposit parameters not provided in correct format | Modified input file to include account number and amount on separate lines |
| test9 | Standard withdrawal transaction | Expected withdraw but command mismatch | Command keyword inconsistency between tests and implementation | Standardized to “withdrawal” and updated input file accordingly |

## Notes
- Tests were run using `run_tests.sh` against inputs in the `inputs/` directory
- Outputs compared against expected files using `validate_tests.sh`


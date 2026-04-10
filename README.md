# CSCI 3060U - Banking System (Phase 6)

## Integration and Delivery

This project simulates a full 7-day week of operations for a banking system. It integrates a Python Front End and Back End using automated Bash shell scripts, fulfilling the requirements for Phase 6.

### Prerequisites
- Python 3.x
- A Unix-like environment to run Bash `.sh` scripts (Linux, macOS, WSL, or Git Bash for Windows).

### Setup
Ensure that the script files are executable before running them. From the root directory of the project, run:
```bash
chmod +x operation_scripts/*.sh
```

### Running the Weekly Simulation
To run the complete 7-day automated simulation, execute the `weekly.sh` script from the project root:
```bash
./operation_scripts/weekly.sh
```

### How it Works
1. **Initialization**: The script uses `data/master_accounts_day0.txt` and `data/current_accounts_day0.txt` as the foundational starting state for Day 1.
2. **Daily Execution (`daily.sh`)**: For each day (1 through 7), the script runs:
   - The Front End for various pre-scripted user sessions (reading automated inputs from `operation_scripts/input/dayX_sessionY.txt`).
   - Merges the multiple daily transaction session files into a single batch file.
   - Runs the Back End to apply those transactions and generate the next day's master and current accounts files.
3. **Outputs**: All generated transaction files, working files, and End-of-Day master/current account files are safely stored in the `operation_scripts/output/` directory, organized sequentially by day.
4. **Automated Verification**: At the very end of Day 7, the script triggers `verify_balances.sh`. This test suite automatically scans the final output files to assert the system behaved perfectly.
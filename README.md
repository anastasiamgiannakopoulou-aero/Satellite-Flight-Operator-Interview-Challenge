# Satellite-Flight-Operator-Interview-Challenge

This is a simple Python simulation of the Flight Operational Contact Procedure prepared for the interview challenge.
It is intentionally written at a basic scripting level. The purpose is to demonstrate the operational logic and decision-making, not advanced Python programming.

# Procedure automated

The script follows the Contact Plan:
1. Contact starts / TX ON
2. Initial spacecraft health check
3. Payload data transfer — Priority 1
4. Platform data transfer — Priority 2
5. Communications configuration upload
6. Communications Subsystem restart
7. TX Modulation restoration
8. Final verification
9. End-of-contact recording and handover

It also includes:
- checks of the remaining contact time
- simple recovery actions
- a contingency margin
- different failure scenarios

# Requirements
Python 3 is required.
No additional Python libraries are required.

# How to run
# Windows

Open Command Prompt or PowerShell in the folder and run:
    python flight_operator_automation.py

If that does not work:
    py flight_operator_automation.py

# Linux / macOS
    python3 flight_operator_automation.py

# Testing different situations
At the top of `flight_operator_automation.py` there is one variable:
    SCENARIO = "normal"

For the normal procedure, leave it as:
    SCENARIO = "normal"

To test a failure, change it to one of:
    "health_fail"
    "payload_fail"
    "platform_fail"
    "config_fail"
    "restart_fail"
    "tx_fail"

Example:
    SCENARIO = "config_fail"

Then run the script again.
This is deliberately simple: there is no command-line framework or external package. The scenario is changed directly in the script so that the logic is easy to inspect and explain.

# How the timing works
The program does not wait for ten real minutes.
Instead, `time_used` represents the simulated time in the contact.

For example:
    use_time(PAYLOAD_TIME)

adds the planned 240 seconds for the payload transfer.

The function:
    time_remaining()

calculates how much of the 600-second contact is still available.

This allows the script to make a basic operational decision:
- if enough time remains, continue or retry
- if not enough time remains, defer the activity

# Important note about commands
The command names such as:
    TX_ON
    RESTART_COMMS_SUBSYSTEM
    RESTORE_TX_MODULATION
are simulated command labels created for the challenge.

They are not claimed to be real command identifiers.
The challenge does not provide actual spacecraft command syntax, so the script does not invent real command interfaces.

# Files

- `flight_operator_automation.py` — main executable script
- `README.md` — instructions
- `run_windows.bat` — optional Windows launcher
- `run_unix.sh` — optional Linux/macOS launcher

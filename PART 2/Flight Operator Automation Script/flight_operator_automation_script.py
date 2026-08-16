"""
Satellite Flight Operator Challenge
Simple automation of the Flight Operational Contact Procedure.

"""
# SETTINGS / ASSUMPTIONS

# Change this value to test a different situation.
# "normal" = nominal contact
# "health_fail" = health check fails
# "payload_fail" = payload transfer fails
# "platform_fail" = platform transfer fails
# "config_fail" = configuration upload fails
# "restart_fail" = COMMS restart fails
# "tx_fail" = TX Modulation restoration fails
SCENARIO = "normal"

CONTACT_TIME = 600       # 10 minutes 
time_used = 0            # Keeps track of the simulated contact time

# Time allocated to each activity, based on the Contact Plan.
HEALTH_TIME = 60
PAYLOAD_TIME = 240
PLATFORM_TIME = 80
CONFIG_TIME = 30
RESTART_TIME = 90
TX_RESTORE_TIME = 40
FINAL_CHECK_TIME = 40
CONTINGENCY_TIME = 20

# HELPER FUNCTIONS

def print_action(message):
    """Print an operator action."""
    print("[OPERATOR] " + message)

def print_command(command):
    """Print a simulated spacecraft command."""
    print("[COMMAND]  " + command)

def print_result(message):
    """Print the expected result."""
    print("[RESULT]   " + message)

def use_time(seconds):
    """
    Add simulated time to the contact.
    The script does not actually wait; it only tracks the time budget.
    """
    global time_used
    time_used = time_used + seconds

def time_remaining():
    """Return the remaining contact time."""
    return CONTACT_TIME - time_used

# START OF CONTACT

print("SATELLITE FLIGHT OPERATOR - PROCEDURE AUTOMATION")

print_action("Contact starts at AOS.")
print_action("Communications are assumed to be full-duplex and RX is ON.")
# TX is commanded ON because the Contact Plan states that TX is commanded ON when required
print_command("TX_ON")
print_result("TX is ON and telemetry is available.")

use_time(0)

# INITIAL HEALTH CHECK

print("\n STEP 1: INITIAL HEALTH CHECK ")

print_action("Check spacecraft telemetry.")
print_action("Review mode, power, thermal, AOCS and Communications status.")

use_time(HEALTH_TIME)
# The failure scenario is only used to demonstrate the recovery path.
if SCENARIO == "health_fail":
    print_result("Telemetry is unexpected or invalid.")
    print_action("Pause the nominal procedure and assess spacecraft state.")
    print_action("Do not continue with non-essential commanding.")
else:
    print_result("Spacecraft health is within expected conditions.")

# If the health check failed, the rest of the nominal sequence should not be executed
if SCENARIO == "health_fail":
    print_action("End contact with incomplete activities recorded.")
else:
    # PAYLOAD DATA - PRIORITY 1

    print("\n STEP 2: PAYLOAD DATA TRANSFER ")

    print_action("Start payload-data download.")
    print_action("Monitor downlink and transfer progress.")

    use_time(PAYLOAD_TIME)
    if SCENARIO == "payload_fail":

        print_result("Payload transfer failed.")
        print_action("Verify link and transfer status.")

        # A retry is only attempted if enough time remains.
        if time_remaining() >= 20:
            print_command("RETRY_PAYLOAD_TRANSFER")
            use_time(20)
            print_result("Payload retry completed.")
        else:
            print_action("Insufficient time for a controlled retry.")
            print_action("Defer remaining payload data to the next contact.")
    else:
        print_result("Payload data transfer completed successfully.")
   
    # PLATFORM DATA - PRIORITY 2

    print("\n STEP 3: PLATFORM DATA TRANSFER ")

    print_action("Start housekeeping data download.")
    print_action("Continue monitoring the downlink.")

    use_time(PLATFORM_TIME)
    if SCENARIO == "platform_fail":

        print_result("Platform data transfer failed.")
        print_action("Verify link and transfer status.")
        if time_remaining() >= 20:
            print_command("RETRY_PLATFORM_TRANSFER")
            use_time(20)
            print_result("Platform retry completed.")
        else:
            print_action("Defer remaining platform data.")
    else:
        print_result("Platform data transfer completed successfully.")
  
    # COMMUNICATIONS CONFIGURATION UPLOAD

    print("\n STEP 4: COMMUNICATIONS CONFIGURATION ")
    # Before starting the configuration change, check whether enough time remains for the whole remaining sequence
    required_time = (
        CONFIG_TIME
        + RESTART_TIME
        + TX_RESTORE_TIME
        + FINAL_CHECK_TIME
        + CONTINGENCY_TIME
    )

    if time_remaining() < required_time:
        print_action(
            "Not enough time remains to safely complete the COMMS change."
        )
        print_action("Defer the configuration change to the next contact.")
    else:
        print_action("Upload the approved Communications configuration.")
        use_time(CONFIG_TIME)
        if SCENARIO == "config_fail":

            print_result("Configuration upload failed.")
            print_action("Verify upload status and file acknowledgement.")

            if time_remaining() >= 20:
                print_command("RETRY_COMMS_CONFIGURATION_UPLOAD")
                use_time(20)
                print_result("Configuration upload retry completed.")
            else:
                print_action(
                    "Abort the configuration change and keep the current configuration."
                )
        else:
            print_result("Configuration upload verified successfully.")

            # COMMUNICATIONS SUBSYSTEM RESTART
            print("\n STEP 5: COMMUNICATIONS SUBSYSTEM RESTART ")

            print_action("Command the Communications Subsystem restart.")
            print_action("Expected effect: temporary loss of downlink.")
            use_time(RESTART_TIME)
            print_command("RESTART_COMMS_SUBSYSTEM")

            if SCENARIO == "restart_fail":
                print_result("COMMS subsystem did not recover as expected.")
                print_action("Assess subsystem status and follow recovery procedure.")
                print_action("Avoid repeated blind commands.")
            else:
                print_result("COMMS subsystem recovered as expected.")

                # RESTORE TX MODULATION

                print("\n STEP 6: RESTORE TX MODULATION ")
                print_action("Command TX Modulation restoration.")
                use_time(TX_RESTORE_TIME)
                print_command("RESTORE_TX_MODULATION")
                if SCENARIO == "tx_fail":

                    print_result("TX Modulation was not restored.")
                    print_action("Verify TX and Communications status.")

                    if time_remaining() >= 20:
                        print_command("RETRY_TX_MODULATION_RESTORE")
                        use_time(20)
                        print_result("Controlled retry completed.")
                    else:
                        print_action(
                            "Do not continue non-essential commanding. "
                            "Record the degraded state."
                        )
                else:
                    print_result(
                        "TX Modulation restored and valid downlink telemetry received."
                    )
    # FINAL VERIFICATION
    print("\n STEP 7: FINAL VERIFICATION ")
    # Only perform this if enough time remains.
    if time_remaining() >= FINAL_CHECK_TIME:

        print_action("Confirm final spacecraft and COMMS state.")
        print_action("Record completed, incomplete and deferred activities.")
        use_time(FINAL_CHECK_TIME)
        print_result("Final state recorded.")
    else:

        print_action("Insufficient time for the planned final verification.")
        print_action("Record the current state for handover.")

# END OF CONTACT
print("\n END OF CONTACT ")
# The remaining time is the contingency margin if it has not been used.
remaining = time_remaining()
if remaining > 0:
    print_action(
        "Remaining contact time: " + str(remaining) + " seconds."
    )
    print_action(
        "This time is available as contingency margin for unexpected delays."
    )
print_action("Record completed / incomplete / deferred activities.")
print_action("Prepare handover for the next contact.")
print_action("Contact ends at LOS.")

print("\nSimulation complete.")

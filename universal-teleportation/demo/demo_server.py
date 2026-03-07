"""
WekezaOmniOS Demo Application: The Background Server
Simulates a stateful service that persists data to a log file.
Used to verify File Descriptor (FD) restoration during teleportation.
"""

import time
import logging
import os

# Ensure the log file is created in a predictable location
LOG_FILE = "demo_server.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [demo_server] %(message)s"
)

def main():
    counter = 0
    print(f"[demo_server] Background service started.")
    print(f"[demo_server] Logging to: {os.path.abspath(LOG_FILE)}")
    print(f"[demo_server] Tick interval: 5 seconds.")
    print("-" * 50)

    try:
        while True:
            counter += 1
            log_msg = f"Server heartbeat tick {counter}"
            
            # Write to disk (Audit Trail simulation)
            logging.info(log_msg)
            
            # Print to stdout for visibility
            print(f"[demo_server] {log_msg}")
            
            time.sleep(5)
    except KeyboardInterrupt:
        print("\n[demo_server] Server shutting down.")

if __name__ == "__main__":
    main()

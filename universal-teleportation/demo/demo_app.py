"""
WekezaOmniOS Demo Application: The Counter
A simple, stateful process used to verify memory persistence during teleportation.
"""

import time
import sys

def main():
    counter = 0
    print(f"[demo_app] Starting WekezaOmniOS Demo App...")
    print(f"[demo_app] Logic: Increment counter every 2 seconds.")
    print(f"[demo_app] PID: {sys.argv[0]} is active. Ready for capture.")
    print("-" * 50)

    try:
        while True:
            counter += 1
            # The goal is to capture the process at 'Tick X' 
            # and have it resume at 'Tick X+1' on the target node.
            print(f"[demo_app] WekezaOmniOS Demo Running | Tick {counter}")
            time.sleep(2)
    except KeyboardInterrupt:
        print("\n[demo_app] Process interrupted by user. Exiting.")

if __name__ == "__main__":
    main()

4️⃣ CLI Interface

Developers interact through CLI first.

cli/

teleport.py
commands.py
teleport.py

Main entry point.

Example usage:

python teleport.py capture 1921

Code:

import sys

def main():

    command = sys.argv[1]

    if command == "capture":
        pid = sys.argv[2]
        print(f"Capturing {pid}")

Example commands:

teleport capture 1921
teleport snapshot 1921
teleport restore snapshot_1921

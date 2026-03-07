# teleport.py
# Main entry point.
# Example usage:
#python teleport.py capture 1921

import sys

def main():

    command = sys.argv[1]

    if command == "capture":
        pid = sys.argv[2]
        print(f"Capturing {pid}")

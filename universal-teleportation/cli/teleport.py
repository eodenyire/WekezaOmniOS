"""
WekezaOmniOS Teleportation CLI
Main entry point for process manipulation.
"""

import sys
from commands import execute_command

def main():
    # Check if a command was actually provided
    if len(sys.argv) < 2:
        print("🚀 WekezaOmniOS Universal Teleportation")
        print("Usage: python teleport.py <command> [args]")
        print("\nAvailable commands: capture, snapshot, restore, status")
        return

    # Separate the specific command from its arguments
    command = sys.argv[1]
    args = sys.argv[2:]

    # Delegate execution to the logic layer
    execute_command(command, args)

if __name__ == "__main__":
    main()

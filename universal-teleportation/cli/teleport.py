"""
WekezaOmniOS Teleportation CLI
Main entry point for process manipulation.
"""

import sys
from commands import execute_command

def main():
    # Welcome message and basic usage help
    if len(sys.argv) < 2:
        print("🚀 WekezaOmniOS Universal Teleportation Engine")
        print("Usage: python teleport.py <command> [args]")
        print("\nAvailable commands:")
        print("  capture <PID>                - Freeze a running process")
        print("  snapshot <PID> [name]        - Create a portable state file")
        print("  restore <snapshot_name>      - Resume a process from state")
        print("  status                       - Check engine health")
        return

    # Separate the specific command from its arguments
    command = sys.argv[1]
    args = sys.argv[2:]

    # Delegate execution to the logic layer in commands.py
    execute_command(command, args)

if __name__ == "__main__":
    main()

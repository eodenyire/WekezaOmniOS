# 📄 `teleport.py`
# Main entry point for the CLI.
import sys
from commands import execute_command

def main():
    if len(sys.argv) < 2:
        print("Usage: python teleport.py <command> [args]")
        return

    command = sys.argv[1]
    args = sys.argv[2:]

    execute_command(command, args)

if __name__ == "__main__":
    main()

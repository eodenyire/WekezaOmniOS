"""
WekezaOmniOS CLI Utilities
Helper functions for input validation and logging formatting.
"""

def validate_pid(pid):
    """Ensures the provided PID is a valid integer."""
    try:
        int_pid = int(pid)
        if int_pid <= 0:
            raise ValueError("PID must be a positive integer.")
        return int_pid
    except ValueError:
        raise ValueError(f"Invalid PID: '{pid}'. Please provide a numeric process ID.")

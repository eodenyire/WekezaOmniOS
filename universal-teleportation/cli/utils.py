def validate_pid(pid):
    try:
        int_pid = int(pid)
        return int_pid
    except ValueError:
        raise ValueError(f"PID must be an integer, got {pid}")

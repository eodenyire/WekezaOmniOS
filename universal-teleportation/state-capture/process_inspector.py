"""
WekezaOmniOS Process Inspector
Gathers telemetry and metadata from the target system process.
"""

import psutil

def get_process_info(pid):
    """
    Retrieves runtime metadata for a given Process ID.
    
    Args:
        pid (int): The Process ID to inspect.
        
    Returns:
        dict: A dictionary containing the process name, status, 
              memory footprint (RSS), and PID.
    """
    try:
        process = psutil.Process(pid)
        
        # Gathering critical process telemetry
        return {
            "pid": pid,
            "name": process.name(),
            "status": process.status(),
            "memory": process.memory_info().rss  # Resident Set Size
        }
    except psutil.NoSuchProcess:
        print(f"[Process Inspector] ERROR: No process found with PID {pid}")
        return None
    except psutil.AccessDenied:
        print(f"[Process Inspector] ERROR: Permission denied for PID {pid}. Run as sudo?")
        return None

# Example usage for manual testing
if __name__ == "__main__":
    import sys
    
    # Use PID from command line or default to current process for testing
    target_pid = int(sys.argv[1]) if len(sys.argv) > 1 else psutil.Process().pid
    
    info = get_process_info(target_pid)
    if info:
        print(f"[Process Inspector] Data retrieved: {info}")

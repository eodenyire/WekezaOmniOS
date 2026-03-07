# Gets process information.
# Example:

import psutil

def get_process_info(pid):
    process = psutil.Process(pid)
    return {
        "name": process.name(),
        "status": process.status(),
        "memory": process.memory_info().rss
    }

🔧 Module Breakdown
1️⃣ state-capture

Captures running process state.

Functions:

capture_memory()
capture_cpu_state()
capture_file_handles()
capture_threads()

Technologies to study:

CRIU (Checkpoint Restore in Userspace)

ptrace

1️⃣ state-capture

Responsible for capturing process state.

state-capture/

capture_manager.py
process_inspector.py
criu_wrapper.py
utils.py
capture_manager.py

Main logic controlling checkpoint.

Example:

class CaptureManager:

    def capture_process(self, pid):
        print(f"Capturing process {pid}")
process_inspector.py

Gets process information.

Example:

import psutil

def get_process_info(pid):
    process = psutil.Process(pid)
    return {
        "name": process.name(),
        "status": process.status(),
        "memory": process.memory_info().rss
    }
criu_wrapper.py

Interface to CRIU commands.

Uses subprocess.

Example:

import subprocess

def checkpoint_process(pid, directory):

    cmd = [
        "criu",
        "dump",
        "-t", str(pid),
        "-D", directory,
        "--shell-job"
    ]

    subprocess.run(cmd)

"""
WekezaOmniOS CRIU Wrapper
Low-level system interface for Checkpoint/Restore in Userspace (CRIU).
"""

import subprocess
import os

def checkpoint_process(pid, directory):
    """
    Interfaces with the system's CRIU binary to dump the state of a 
    running process into a specified directory.
    
    Args:
        pid (int): The Process ID of the target application.
        directory (str): The local path where checkpoint images will be saved.
    """
    # 1. Prepare the workspace
    # Ensuring the directory exists prevents CRIU from failing immediately
    os.makedirs(directory, exist_ok=True)

    # 2. Construct the CRIU dump command
    # -t: Target PID
    # -D: Destination directory for images
    # --shell-job: Allows checkpointing processes started from a shell
    # --leave-running: Keeps the source process alive after the dump (crucial for Phase 1 testing)
    cmd = [
        "criu",
        "dump",
        "-t", str(pid),
        "-D", directory,
        "--shell-job",
        "--leave-running" 
    ]

    print(f"[CRIU Wrapper] Executing system dump: {' '.join(cmd)}")

    # 3. Execution with Error Handling
    try:
        # check=True ensures an exception is raised if CRIU returns a non-zero exit code
        subprocess.run(cmd, check=True)
        print(f"[CRIU Wrapper] SUCCESS: Checkpoint images written to {directory}")
    except subprocess.CalledProcessError as e:
        print(f"[CRIU Wrapper] CRITICAL ERROR: CRIU failed with exit code {e.returncode}")
        print("[CRIU Wrapper] Check if you have sudo privileges and if the process is 'dumpable'.")
        raise
    except FileNotFoundError:
        print("[CRIU Wrapper] ERROR: 'criu' binary not found. Is it installed on this node?")
        raise

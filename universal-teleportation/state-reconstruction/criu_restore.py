"""
WekezaOmniOS CRIU Restore Wrapper
Low-level interface to the Checkpoint/Restore in Userspace (CRIU) utility.
"""

import subprocess
import os

def restore_process(directory):
    """
    Executes the CRIU restore command to resume a process from its checkpointed state.
    
    Args:
        directory (str): The path to the directory containing the checkpoint images.
    """
    # 1. Integrity Check: Ensure CRIU has a valid source to read from
    if not os.path.exists(directory):
        error_msg = f"Snapshot directory does not exist: {directory}"
        print(f"[CRIU Restore] ERROR: {error_msg}")
        raise FileNotFoundError(error_msg)

    # 2. Command Construction
    # --shell-job: Allows restoring processes that were started from a shell
    cmd = [
        "criu",
        "restore",
        "-D", directory,
        "--shell-job"
    ]

    print(f"[CRIU Restore] Initiating system-level restore: {' '.join(cmd)}")

    # 3. Execution
    try:
        # check=True raises a CalledProcessError if the restore fails (e.g., PID conflict)
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"[CRIU Restore] CRITICAL: Process restoration failed. Exit code: {e.returncode}")
        raise
    except Exception as e:
        print(f"[CRIU Restore] UNEXPECTED ERROR: {str(e)}")
        raise

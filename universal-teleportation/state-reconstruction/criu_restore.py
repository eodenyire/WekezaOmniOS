"""
WekezaOmniOS CRIU Restore Wrapper
Low-level interface to the Checkpoint/Restore in Userspace (CRIU) utility.
"""

import subprocess
import os
import json

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

    # 2. Check if this is a fallback snapshot
    fallback_marker = os.path.join(directory, "FALLBACK_MODE.txt")
    if os.path.exists(fallback_marker):
        print(f"[CRIU Restore] ⚠️  This is a fallback snapshot (metadata-only)")
        return _fallback_restore(directory)

    # 3. Check if CRIU is available
    try:
        subprocess.run(["which", "criu"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("[CRIU Restore] ⚠️  CRIU not available. Cannot restore process state.")
        print("[CRIU Restore] Showing captured metadata instead...")
        return _fallback_restore(directory)

    # 4. Command Construction
    # --shell-job: Allows restoring processes that were started from a shell
    cmd = [
        "criu",
        "restore",
        "-D", directory,
        "--shell-job"
    ]

    print(f"[CRIU Restore] Initiating system-level restore: {' '.join(cmd)}")

    # 5. Execution
    try:
        # check=True raises a CalledProcessError if the restore fails (e.g., PID conflict)
        subprocess.run(cmd, check=True)
        print(f"[CRIU Restore] ✅ Process restored successfully")
    except subprocess.CalledProcessError as e:
        print(f"[CRIU Restore] ⚠️  Process restoration failed. Exit code: {e.returncode}")
        print("[CRIU Restore] This is expected in dev containers or without proper privileges")
        return _fallback_restore(directory)
    except Exception as e:
        print(f"[CRIU Restore] ERROR: {str(e)}")
        raise

def _fallback_restore(directory):
    """
    Fallback mechanism when CRIU is unavailable or snapshot is metadata-only.
    Displays the captured process information.
    """
    print(f"[CRIU Restore] 📋 Displaying captured metadata from {directory}...")
    
    try:
        # Load process metadata
        metadata_file = os.path.join(directory, "process_metadata.json")
        if os.path.exists(metadata_file):
            with open(metadata_file, "r") as f:
                metadata = json.load(f)
            
            print("[CRIU Restore] Captured Process Information:")
            print(f"  PID: {metadata.get('pid')}")
            print(f"  Name: {metadata.get('name')}")
            print(f"  Status: {metadata.get('status')}")
            print(f"  Memory (RSS): {metadata.get('memory_rss', 0) / 1024 / 1024:.2f} MB")
            print(f"  CPU: {metadata.get('cpu_percent')}%")
            print(f"  Working Directory: {metadata.get('cwd')}")
            print(f"  Command: {' '.join(metadata.get('cmdline', []))}")
        
        # Load environment
        env_file = os.path.join(directory, "env.json")
        if os.path.exists(env_file):
            with open(env_file, "r") as f:
                env = json.load(f)
            print(f"\n[CRIU Restore] Captured {len(env)} environment variables")
        
        # Check for fallback marker
        fallback_marker = os.path.join(directory, "FALLBACK_MODE.txt")
        if os.path.exists(fallback_marker):
            with open(fallback_marker, "r") as f:
                print(f"\n[CRIU Restore] {f.read()}")
        
        print(f"\n[CRIU Restore] ✅ Metadata displayed successfully")
        print(f"[CRIU Restore] Note: Install CRIU and run with proper privileges for full restoration")
        
    except Exception as e:
        print(f"[CRIU Restore] ERROR reading metadata: {e}")
        raise

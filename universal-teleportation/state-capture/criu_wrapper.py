"""
WekezaOmniOS CRIU Wrapper
Low-level system interface for Checkpoint/Restore in Userspace (CRIU).
"""

import subprocess
import os
import json
import psutil

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

    # 2. Check if CRIU is available
    try:
        subprocess.run(["which", "criu"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("[CRIU Wrapper] ⚠️  CRIU not available. Using fallback snapshot mode...")
        return _fallback_checkpoint(pid, directory)

    # 3. Construct the CRIU dump command
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

    # 4. Execution with Error Handling
    try:
        # check=True ensures an exception is raised if CRIU returns a non-zero exit code
        subprocess.run(cmd, check=True)
        print(f"[CRIU Wrapper] SUCCESS: Checkpoint images written to {directory}")
    except subprocess.CalledProcessError as e:
        print(f"[CRIU Wrapper] ⚠️  CRIU failed with exit code {e.returncode}")
        print("[CRIU Wrapper] Falling back to metadata-only snapshot mode...")
        return _fallback_checkpoint(pid, directory)
    except FileNotFoundError:
        print("[CRIU Wrapper] ERROR: 'criu' binary not found. Using fallback mode...")
        return _fallback_checkpoint(pid, directory)

def _fallback_checkpoint(pid, directory):
    """
    Fallback mechanism when CRIU is unavailable.
    Captures process metadata and environment for demonstration purposes.
    """
    print(f"[CRIU Wrapper] 📋 Creating metadata snapshot for PID {pid}...")
    
    try:
        process = psutil.Process(pid)
        
        # Capture process state
        metadata = {
            "pid": pid,
            "name": process.name(),
            "status": process.status(),
            "memory_rss": process.memory_info().rss,
            "cpu_percent": process.cpu_percent(),
            "cwd": process.cwd(),
            "cmdline": process.cmdline(),
            "create_time": process.create_time(),
        }
        
        # Save metadata
        metadata_file = os.path.join(directory, "process_metadata.json")
        with open(metadata_file, "w") as f:
            json.dump(metadata, f, indent=4)
        
        # Capture environment
        env_file = os.path.join(directory, "env.json")
        with open(env_file, "w") as f:
            json.dump(dict(process.environ()), f, indent=4)
        
        # Create a marker file indicating fallback mode
        marker_file = os.path.join(directory, "FALLBACK_MODE.txt")
        with open(marker_file, "w") as f:
            f.write("This snapshot was created without CRIU.\n")
            f.write("Only metadata and environment variables were captured.\n")
            f.write("Full process state restoration requires CRIU.\n")
        
        print(f"[CRIU Wrapper] ✅ Fallback snapshot created at {directory}")
        print(f"[CRIU Wrapper] Note: Install CRIU for full checkpoint/restore functionality")
        
    except psutil.NoSuchProcess:
        print(f"[CRIU Wrapper] ERROR: Process {pid} not found")
        raise
    except Exception as e:
        print(f"[CRIU Wrapper] ERROR during fallback capture: {e}")
        raise

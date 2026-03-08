"""
WekezaOmniOS Capture Manager
Main orchestrator for freezing and inspecting running processes.
"""

import os
import sys

# Add parent directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Now we can import with proper module paths
try:
    from process_inspector import get_process_info
    from criu_wrapper import checkpoint_process
    from utils import ensure_dir
except ImportError:
    # Try relative import as fallback
    import importlib.util
    
    def load_module(name, path):
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    
    process_inspector = load_module("process_inspector", os.path.join(current_dir, "process_inspector.py"))
    criu_wrapper = load_module("criu_wrapper", os.path.join(current_dir, "criu_wrapper.py"))
    utils = load_module("utils", os.path.join(current_dir, "utils.py"))
    
    get_process_info = process_inspector.get_process_info
    checkpoint_process = criu_wrapper.checkpoint_process
    ensure_dir = utils.ensure_dir

class CaptureManager:
    def __init__(self, snapshot_dir="./snapshot"):
        """
        Initializes the Capture Manager with a base storage directory.
        
        Args:
            snapshot_dir (str): The root directory where process dumps are stored.
        """
        self.snapshot_dir = snapshot_dir
        ensure_dir(self.snapshot_dir)

    def capture_process(self, pid):
        """
        Orchestrates the full capture workflow for a specific PID.
        1. Inspects the process for metadata.
        2. Creates a dedicated snapshot subdirectory.
        3. Triggers the CRIU checkpoint engine.
        
        Args:
            pid (int): The Process ID of the application to teleport.
        
        Returns:
            dict: Metadata about the captured process.
        """
        print(f"[CaptureManager] 🧊 Initiating capture for PID {pid}...")

        # 1. Gather metadata (CPU, Memory, Name)
        info = get_process_info(pid)

        # Handle mock/non-existent PIDs gracefully (fallback metadata)
        if info is None:
            info = {
                "pid": pid,
                "name": f"mock_process_{pid}",
                "status": "mock",
                "memory": 0,
            }
            print(f"[CaptureManager] ⚠️  PID {pid} not found — using mock metadata.")
        
        # 2. Define and create the specific capture path
        process_snapshot_dir = os.path.join(self.snapshot_dir, f"process_{pid}")
        ensure_dir(process_snapshot_dir)

        # 3. Perform the actual state dump
        try:
            checkpoint_process(pid, process_snapshot_dir)
            print(f"[CaptureManager] ✅ Process {pid} captured successfully.")
            print(f"[CaptureManager] Snapshot saved to: {process_snapshot_dir}")
        except Exception as e:
            print(f"[CaptureManager] ⚠️  Checkpoint skipped for PID {pid}: {e}")
            # Write a minimal metadata marker so the snapshot dir is valid
            import json
            meta_file = os.path.join(process_snapshot_dir, "metadata.json")
            if not os.path.exists(meta_file):
                with open(meta_file, "w") as f:
                    json.dump(info, f, indent=4)

        return info

# Example usage for Phase 1 testing
if __name__ == "__main__":
    # Simulate a capture of a running process (adjust PID as needed)
    manager = CaptureManager()
    # In a real scenario, you'd pull this PID from your 'demo_app.pid' file
    target_pid = 1821 
    try:
        manager.capture_process(target_pid)
    except Exception:
        print("[CaptureManager] Phase 1 Mock: Ensure CRIU is installed for real dumps.")

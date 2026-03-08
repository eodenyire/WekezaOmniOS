"""
WekezaOmniOS Restore Manager
Orchestrates the rehydration of captured process snapshots.
"""

import os
import sys
import importlib.util

# Add parent directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Load modules
def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

criu_restore_module = load_module("criu_restore", os.path.join(current_dir, "criu_restore.py"))
environment_loader_module = load_module("environment_loader", os.path.join(current_dir, "environment_loader.py"))

restore_process = criu_restore_module.restore_process
load_environment = environment_loader_module.load_environment

class RestoreManager:
    def __init__(self, snapshot_dir="./snapshot"):
        """
        Initializes the Restore Manager with a target snapshot directory.
        """
        self.snapshot_dir = snapshot_dir

    def restore_snapshot(self, process_id):
        """
        Full orchestration of process restoration:
        1. Locate snapshot directory
        2. Load environment variables
        3. Trigger system-level restore (CRIU)
        """
        # Path where the specific process state is stored
        process_snapshot_dir = os.path.join(self.snapshot_dir, f"process_{process_id}")
        
        # 1. Validation: Ensure the snapshot exists
        if not os.path.exists(process_snapshot_dir):
            error_message = f"Snapshot directory not found: {process_snapshot_dir}"
            print(f"[RestoreManager] ERROR: {error_message}")
            raise FileNotFoundError(error_message)

        # 2. Rehydration: Set up environment variables
        print(f"[RestoreManager] Loading environment for PID {process_id}...")
        env_file_path = os.path.join(process_snapshot_dir, "env.json")
        load_environment(env_file_path)

        # 3. Execution: Call the CRIU restore wrapper
        print(f"[RestoreManager] Restoring process {process_id} from snapshot...")
        restore_process(process_snapshot_dir)
        
        print(f"[RestoreManager] SUCCESS: Process {process_id} has been restored and resumed.")

# Example usage for Phase 1 testing
if __name__ == "__main__":
    # Simulate a restoration of PID 1821
    manager = RestoreManager()
    try:
        manager.restore_snapshot(1821)
    except Exception as e:
        print(f"[RestoreManager] Restore failed: {e}")

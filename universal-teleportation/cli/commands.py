"""
WekezaOmniOS CLI Command Execution Layer
Phase 1: Fully integrated command execution.
"""

import os
import sys
import importlib.util
from utils import validate_pid
import datetime

# Add parent directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Import modules using importlib (to handle hyphenated directory names)
def load_module(name, path):
    """Import a module from a file path."""
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# Import the state management modules
capture_manager_module = load_module(
    "capture_manager",
    os.path.join(parent_dir, "state-capture", "capture_manager.py")
)
snapshot_builder_module = load_module(
    "snapshot_builder",
    os.path.join(parent_dir, "snapshot-engine", "snapshot_builder.py")
)
snapshot_metadata_module = load_module(
    "snapshot_metadata",
    os.path.join(parent_dir, "snapshot-engine", "snapshot_metadata.py")
)
restore_manager_module = load_module(
    "restore_manager",
    os.path.join(parent_dir, "state-reconstruction", "restore_manager.py")
)

CaptureManager = capture_manager_module.CaptureManager
build_snapshot = snapshot_builder_module.build_snapshot
save_metadata = snapshot_metadata_module.save_metadata
RestoreManager = restore_manager_module.RestoreManager

def execute_command(command, args):
    try:
        if command == "capture":
            if not args:
                print("[Error] Capture requires a PID.")
                return
            pid = validate_pid(args[0])
            print(f"[CLI] 🧊 Initiating Freeze-Ray for process {pid}...")
            
            # Initialize and execute capture
            manager = CaptureManager(snapshot_dir="./snapshots")
            try:
                info = manager.capture_process(pid)
                print(f"[CLI] ✅ Process captured successfully: {info}")
            except Exception as e:
                print(f"[CLI] ❌ Capture failed: {e}")
                print("[CLI] Note: CRIU may not be available. Install it or run with sudo privileges.")

        elif command == "snapshot":
            if not args:
                print("[Error] Snapshot requires a PID.")
                return
            pid = validate_pid(args[0])
            snapshot_name = args[1] if len(args) > 1 else f"snapshot_{pid}"
            print(f"[CLI] 📦 Creating snapshot '{snapshot_name}' for process {pid}...")
            
            # Build the snapshot
            snapshot_dir = f"./snapshots/process_{pid}"
            output_file = f"./snapshots/{snapshot_name}.tar.gz"
            
            metadata = {
                "process_id": pid,
                "timestamp": datetime.datetime.now().isoformat(),
                "snapshot_name": snapshot_name,
                "os": "ubuntu-24.04",
                "architecture": "x86_64"
            }
            
            try:
                success = build_snapshot(snapshot_dir, output_file, metadata)
                if success:
                    print(f"[CLI] ✅ Snapshot created: {output_file}")
                else:
                    print(f"[CLI] ❌ Snapshot creation failed")
            except Exception as e:
                print(f"[CLI] ❌ Error creating snapshot: {e}")

        elif command == "restore":
            if not args:
                print("[Error] Restore requires a process ID.")
                return
            pid = validate_pid(args[0])
            print(f"[CLI] ⚡ Reanimating process {pid} from snapshot...")
            
            # Initialize and execute restoration
            manager = RestoreManager(snapshot_dir="./snapshots")
            try:
                manager.restore_snapshot(pid)
                print(f"[CLI] ✅ Process restored successfully")
            except Exception as e:
                print(f"[CLI] ❌ Restore failed: {e}")
                print("[CLI] Note: CRIU may not be available. Install it or run with sudo privileges.")

        elif command == "status":
            print("[CLI] 🏥 Engine Status Check")
            print("[CLI] Phase 1 - Local Process Teleportation")
            
            # Check if directories exist
            dirs = ["./snapshots", "./logs", "./temp", "./demo"]
            for d in dirs:
                status = "✅" if os.path.exists(d) else "❌"
                print(f"[CLI]   {status} Directory: {d}")
            
            # Check for CRIU
            import subprocess
            try:
                subprocess.run(["which", "criu"], check=True, capture_output=True)
                print("[CLI]   ✅ CRIU: installed")
            except:
                print("[CLI]   ⚠️  CRIU: not found (install for full functionality)")
            
            print("[CLI] Status: READY")

        else:
            print(f"[Error] Unknown command '{command}'")
            
    except ValueError as e:
        print(f"[Validation Error] {e}")
    except Exception as e:
        print(f"[Unexpected Error] {e}")

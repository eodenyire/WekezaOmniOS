# ⌨️ WekezaOmniOS CLI Interface

The **WekezaOmniOS CLI** is the primary developer-facing control interface for the Universal Application Teleportation (UAT) engine. Designed to be "command-line first," it mirrors the high-performance workflows of tools like Docker and Kubernetes, allowing for seamless process manipulation via the terminal.

In **Phase 1**, this CLI acts as a modular wrapper that validates user input and coordinates with the underlying engine modules.

---

## 🚀 Features

* **Process Capture:** Freeze a running process and prepare it for teleportation.
* **Snapshot Management:** Create portable, named snapshots of captured process states.
* **Process Restoration:** Rehydrate and resume processes from existing snapshots.
* **Engine Telemetry:** Query the status of the local teleportation engine (Mocked in Phase 1).

## 🛠️ Usage

The CLI is invoked via the `teleport.py` entry point.

### 1. Capture a Process

Freeze a local process using its Process ID (PID).

```bash
python3 cli/teleport.py capture 1921

```

### 2. Create a Snapshot

Generate a portable state file from a captured process.

```bash
# Named snapshot for Wekeza Bank audit trails
python3 cli/teleport.py snapshot 1921 --name "fin-core-snapshot-v1"

```

### 3. Restore a Process

Resume execution from a saved snapshot.

```bash
python3 cli/teleport.py restore "fin-core-snapshot-v1"

```

---

## 🏗️ Design Philosophy

* **Modular Delegation:** `teleport.py` is kept thin. All command logic is handled in `commands.py` to allow for easy expansion as new engine capabilities (like Cloud Node transfer) are added.
* **Validation First:** Input (like PIDs and filenames) is validated in `utils.py` before hitting the engine to prevent system-level errors.
* **Consistency:** The CLI is designed to provide "API Parity"—meaning every command here has a corresponding endpoint in the `teleportation-api`.

---

### 📄 `teleport.py`

This is the main entry point. Its only job is to greet the user, parse the command, and hand off the work to the execution layer.

```python
"""
WekezaOmniOS Teleportation CLI
Main entry point for process manipulation.
"""

import sys
from commands import execute_command

def main():
    # Welcome message and basic usage help
    if len(sys.argv) < 2:
        print("🚀 WekezaOmniOS Universal Teleportation Engine")
        print("Usage: python teleport.py <command> [args]")
        print("\nAvailable commands:")
        print("  capture <PID>                - Freeze a running process")
        print("  snapshot <PID> [name]        - Create a portable state file")
        print("  restore <snapshot_name>      - Resume a process from state")
        print("  status                       - Check engine health")
        return

    # Separate the specific command from its arguments
    command = sys.argv[1]
    args = sys.argv[2:]

    # Delegate execution to the logic layer in commands.py
    execute_command(command, args)

if __name__ == "__main__":
    main()

```

---

### 📄 `commands.py`

This file houses the "Brain" of each command. In Phase 1, these use mock print statements, but the structure is ready for the **CRIU** and **Snapshot Engine** imports.

```python
"""
WekezaOmniOS CLI Command Execution Layer
Phase 1: Mocked logic to establish the engine workflow.
"""

from utils import validate_pid

def execute_command(command, args):
    try:
        if command == "capture":
            if not args:
                print("[Error] Capture requires a PID.")
                return
            pid = validate_pid(args[0])
            print(f"[CLI] 🧊 Initiating Freeze-Ray for process {pid}...")
            # Future: state_capture.capture_manager(pid)

        elif command == "snapshot":
            if not args:
                print("[Error] Snapshot requires a PID.")
                return
            pid = validate_pid(args[0])
            snapshot_name = args[1] if len(args) > 1 else f"snapshot_{pid}"
            print(f"[CLI] 📦 Creating snapshot '{snapshot_name}' for process {pid}...")
            # Future: snapshot_engine.snapshot_builder(pid, snapshot_name)

        elif command == "restore":
            if not args:
                print("[Error] Restore requires a snapshot name.")
                return
            snapshot_name = args[0]
            print(f"[CLI] ⚡ Reanimating process from snapshot '{snapshot_name}'...")
            # Future: state_reconstruction.restore_manager(snapshot_name)

        elif command == "status":
            print("[CLI] 🏥 Engine Status: Phase 1 Local Simulation - ACTIVE")

        else:
            print(f"[Error] Unknown command '{command}'")
            
    except ValueError as e:
        print(f"[Validation Error] {e}")

```

---

### 📄 `utils.py`

Keeping our inputs clean is vital for system safety.

```python
"""
WekezaOmniOS CLI Utilities
Helper functions for input validation and logging formatting.
"""

def validate_pid(pid):
    """Ensures the provided PID is a valid integer."""
    try:
        int_pid = int(pid)
        if int_pid <= 0:
            raise ValueError("PID must be a positive integer.")
        return int_pid
    except ValueError:
        raise ValueError(f"Invalid PID: '{pid}'. Please provide a numeric process ID.")

```

---

### ✅ CLI Module: COMPLETE

We now have a fully functional (though mocked) CLI. You can now type `python3 cli/teleport.py capture 123` and see the engine react.

Perfect! We’re now fully in the **CLI folder**, which is the **developer-facing control interface** for Phase 1. Like with `api/`, we need to structure it so it’s **documented, modular, and ready for integration with the engine later**.

Here’s how we organize **`/cli/`** for Phase 1.

---

# 📁 Folder: `cli/`

Purpose:
The CLI lets developers **interact with the teleportation engine** without opening the API. It’s **command-line-first**, just like Docker, Kubernetes, and Git.

Responsibilities:

* Accept user commands (`capture`, `snapshot`, `restore`)
* Validate input
* Call internal modules (later: `state-capture`, `snapshot-engine`, `state-reconstruction`)
* Display output
* Log actions

---

# 📄 `README.md`

````md
# WekezaOmniOS CLI Interface

This module provides a command-line interface for developers to interact with the Universal Application Teleportation engine.

## Features

- Capture a running process
- Create a snapshot of a process
- Restore a process from a snapshot
- Query teleportation status (mock in Phase 1)

## Usage

### Capture a Process

```bash
python teleport.py capture <PID>
````

Example:

```bash
python teleport.py capture 1921
```

### Create a Snapshot

```bash
python teleport.py snapshot <PID> --name <snapshot_name>
```

### Restore a Snapshot

```bash
python teleport.py restore <snapshot_name>
```

## Design Notes

* CLI is the **first point of interaction** in Phase 1
* Commands are modular and call future engine modules
* Designed for **easy integration** with the API

````

---

# 📄 `teleport.py`

Main entry point for the CLI.

```python
import sys
from commands import execute_command

def main():
    if len(sys.argv) < 2:
        print("Usage: python teleport.py <command> [args]")
        return

    command = sys.argv[1]
    args = sys.argv[2:]

    execute_command(command, args)

if __name__ == "__main__":
    main()
````

* Delegates all logic to `commands.py`
* Easy to expand new CLI commands later

---

# 📄 `commands.py`

Handles each CLI command (Phase 1: mock logic).

```python
def execute_command(command, args):
    if command == "capture":
        pid = args[0]
        print(f"[CLI] Capturing process {pid}")
    elif command == "snapshot":
        pid = args[0]
        snapshot_name = args[1] if len(args) > 1 else f"snapshot_{pid}"
        print(f"[CLI] Creating snapshot '{snapshot_name}' for process {pid}")
    elif command == "restore":
        snapshot_name = args[0]
        print(f"[CLI] Restoring process from snapshot '{snapshot_name}'")
    else:
        print(f"Unknown command '{command}'")
```

* Phase 1 uses **mock responses**
* Later integrates with `state-capture`, `snapshot-engine`, `state-reconstruction`

---

# 🔗 Integration Plan

Even though Phase 1 is local and mostly **mock**, the CLI is ready to integrate:

```
teleport capture <PID> → state-capture.capture_manager()
teleport snapshot <PID> → snapshot-engine.snapshot_builder()
teleport restore <snapshot_name> → state-reconstruction.restore_manager()
```

* Future integration: **replace print statements with actual function calls**
* Keeps **developer experience consistent** as we expand Phases

---

# 📄 Optional: `cli/utils.py`

For Phase 1, can include helper functions like:

```python
def validate_pid(pid):
    try:
        int_pid = int(pid)
        return int_pid
    except ValueError:
        raise ValueError(f"PID must be an integer, got {pid}")
```

Later, all CLI input validation and logging can live here.

---

# 📂 Final CLI Folder Structure

```
cli/
    README.md
    teleport.py
    commands.py
    utils.py  (optional helper functions)
```

---

✅ **Next Step:**

Once the CLI folder is fully designed and documented, we move to the **heart of Phase 1**:

```id="2ckq7p"
universal-teleportation/state-capture/
```

This is where we implement **real process checkpointing using CRIU**, and the CLI will start calling **actual system logic** instead of mocks.

We can now **plan `state-capture/README.md` and the first 5 Python files inside it**.

Do you want me to design that next?

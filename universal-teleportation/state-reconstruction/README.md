# 🏗️ WekezaOmniOS: State Reconstruction

The **State Reconstruction** module is responsible for the second half of the teleportation loop. It takes a portable process snapshot and rehydrates it into a fully functional, running process on the target environment.

By integrating with **CRIU (Checkpoint/Restore in Userspace)**, this module ensures that a process resumes exactly where it left off, maintaining its memory state, open file handles, and execution context.

---

## 🎯 Purpose & Capabilities

The reconstruction engine ensures that the "teleported" application is indistinguishable from the original.

* **Memory Rehydration:** Restores the exact memory pages and CPU registers of the captured process.
* **Thread Recovery:** Re-establishes execution threads and process hierarchy.
* **Environment Inversion:** Injects the original environment variables using the `EnvironmentLoader`.
* **Seamless Resumption:** Triggers the kernel to resume execution without the application realizing it was ever paused.

---

## 📂 Module Structure

| File | Responsibility |
| --- | --- |
| **`restore_manager.py`** | The main orchestrator. It coordinates the setup and triggers the restore sequence. |
| **`criu_restore.py`** | A system wrapper that handles the low-level CLI calls to the CRIU binary. |
| **`environment_loader.py`** | Specifically handles the parsing and injection of `env.json` into the OS. |

---

## 🔄 Restoration Workflow

The `RestoreManager` follows a strict three-step protocol to ensure system stability:

1. **Identity Verification:** The engine locates the process-specific folder within the `snapshot/` directory using the provided Snapshot ID.
2. **Context Loading:** The `EnvironmentLoader` parses the captured environment and populates the current execution shell to ensure the app has its required config.
3. **Process Reanimation:** The `CriuRestore` wrapper triggers the system-level command. At this point, the process "teleports" from the disk back into the CPU's execution queue.

---

## 🛠️ Usage Example

This module is typically called by the **Teleportation API** or the **CLI** after the `Transfer Layer` has delivered the snapshot cargo.

```python
from state_reconstruction.restore_manager import RestoreManager

# Initialize the manager with the target storage path
manager = RestoreManager(snapshot_dir="./snapshots")

# Restore process 1821 from its local snapshot
manager.restore_snapshot(process_id=1821)

```

---

## 🔗 Integration Plan

* **Upstream:** Receives verified and transferred snapshots from the **Transfer Layer**.
* **Downstream:** Produces a running process that is monitored by the **Monitoring Module**.
* **Logging:** All restoration events, whether successful or failed, are recorded in `logs/restore.log`.

---

### ✅ Phase 1 Complete

With the **State Reconstruction** folder finalized, you now have a complete, documented, and modular blueprint for **Universal Application Teleportation Phase 1**. Every component—from the high-level API to the low-level CRIU wrappers—is ready for execution.

# 🧊 WekezaOmniOS: State Capture

The **State Capture** module is the heartbeat of the Phase 1 bootstrapping process. Its primary mission is to perform a "deep freeze" of a running application, capturing its entire runtime state—memory, CPU registers, instruction pointers, and file handles—so it can be reanimated later in a different environment.

This module acts as the bridge between the high-level **Teleportation API** and the low-level Linux kernel interfaces.

---

## 🎯 Features & Capabilities

* **Full-State Checkpointing:** Leverages **CRIU** (Checkpoint/Restore in Userspace) to dump the process image.
* **Telemetry Inspection:** Uses `psutil` to gather metadata (RSS memory, thread counts, status) for the snapshot manifest.
* **Resource Preservation:** Captures open file descriptors and socket states to ensure continuity.
* **Execution Modes:** Supports `--leave-running` for "cloning" teleportation or full migration.

---

## 📁 Module Breakdown & Responsibilities

| File | Responsibility |
| --- | --- |
| **`capture_manager.py`** | The central orchestrator. It manages the handoff between inspection and the actual system dump. |
| **`process_inspector.py`** | The "Eyes" of the module. Retrieves the metadata needed for the `snapshot-engine`. |
| **`criu_wrapper.py`** | The "Muscle." A low-level interface that executes the `criu dump` system commands. |
| **`utils.py`** | The "Foundation." Handles path validation, directory creation, and serialization helpers. |

---

## 🔄 The Capture Workflow

1. **Selection:** `CaptureManager` receives a PID from the CLI or API.
2. **Telemetry:** `process_inspector` queries the OS to verify the process is healthy and to record its memory footprint.
3. **Preparation:** `utils` ensures a dedicated workspace exists in the `./snapshot/` directory.
4. **The Freeze:** `criu_wrapper` signals the kernel to dump the process's memory pages to disk.
5. **Handoff:** The resulting raw image files are passed to the **Snapshot Engine** for compression.

---

## 🛠️ Phase 1 Internal API Example

```python
from state_capture.capture_manager import CaptureManager

# Initialize the manager pointing to the central snapshot warehouse
manager = CaptureManager(snapshot_dir="./snapshot")

# Capture a process (e.g., a running Python script)
# This will create a directory: ./snapshot/process_1821/
metadata = manager.capture_process(pid=1821)

print(f"Captured {metadata['name']} using {metadata['memory']} bytes.")

```

---

## 🔗 Integration Plan

The State Capture module is the entry point of the **Universal Application Teleportation (UAT)** pipeline:

> **State Capture** ⮕ **Snapshot Engine** ⮕ **Transfer Layer** ⮕ **State Reconstruction**

* **Upstream:** Triggered by the **Teleportation API** or **CLI**.
* **Downstream:** Feeds raw memory dumps to the **Snapshot Engine** for packaging.
* **Technologies:** Built on `psutil`, `subprocess`, and `CRIU`.

---

### ✅ Module Status: PHASE 1 COMPLETE

With the completion of this module, **WekezaOmniOS** now possesses the ability to stop time for any process on a Linux-based environment.

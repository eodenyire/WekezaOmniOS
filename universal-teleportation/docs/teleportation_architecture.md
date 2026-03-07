### 🏗️ Deep-Dive: Engine Internals

This document details the low-level execution flow and the handoff mechanisms between modules.

## ⚙️ Core Engine Modules

| Module | Internal Function | Tech Stack |
| --- | --- | --- |
| **`state-capture/`** | Intersects process memory and registers. | `CRIU`, `ptrace`, `psutil` |
| **`snapshot-engine/`** | Serializes binary dumps and environment state. | `tarfile`, `json`, `hashlib` |
| **`state-reconstruction/`** | Rehydrates the process in a new address space. | `CRIU restore`, `os.execve` |
| **`cluster/`** | Discovers and validates target node readiness. | `FastAPI`, `ZeroMQ` |

## 🔄 The Teleportation Lifecycle (Internal Flow)

1. **Request Ingestion:** The `teleportation-api` receives a PID and a Target Node ID.
2. **Pre-Flight Check:** `cluster_manager` pings the target node to ensure the **Runtime Adapter** (e.g., Linux vs. Windows) matches the `metadata.json`.
3. **The Freeze (Capture):** `capture_manager` calls the `criu_wrapper` to dump memory pages to the `temp/` workspace.
4. **The Package (Snapshot):** `snapshot_builder` compresses the memory dump and attaches the `env.json` and `metadata.json`.
5. **The Jump (Transfer):** (Phase 2) The `transfer-layer` moves the `.tar.gz` to the target node.
6. **The Thaw (Reconstruct):** `restore_manager` extracts the cargo and re-executes the process image.
7. **Handshake:** The monitoring module confirms the process is `RUNNING` on the new node and closes the log entry.

## 🚀 Future Integration Roadmap

* **Distributed Engines:** Support for multiple capture nodes across different geographic locations.
* **Kernel-Level Hooks:** Moving from userspace `CRIU` to dedicated kernel modules for sub-millisecond teleportation.

---

# 📂 Folder: `logs/`

We are now moving to the **Logs** folder. In systems engineering, **Rule 5: Everything Must Be Observable** is non-negotiable. If a teleportation fails at a 99% progress bar, the logs are the only way we find out why.

### 📄 `README.md` (Logs & Conventions)

```markdown
# 📜 WekezaOmniOS: Logging & Observability

This folder contains the audit trail for every action performed by the UAT engine.

## ⚖️ Rule 5 — Everything Must Be Observable
Systems software must produce logs. In Phase 1, we establish a structured logging convention that allows for easy debugging and future integration with ELK or Prometheus stacks.

## 📁 Log Structure
- `teleport.log`: The master audit trail for the full lifecycle.
- `capture.log`: Detailed output from the checkpointing process.
- `restore.log`: Detailed output from the reanimation phase.

## 📝 Logging Conventions
Every entry must include:
1. **Timestamp:** `[YYYY-MM-DD HH:MM:SS]`
2. **Component:** `[CAPTURE]`, `[SNAPSHOT]`, `[RESTORE]`, etc.
3. **Identifier:** The PID of the target process.
4. **Status:** `[INFO]`, `[WARNING]`, or `[ERROR]`.


```

---

### ✅ Next Step: Logging Implementation

The architecture is now fully documented. We have the "Blueprint" and the "Flight Recorder" structure ready.

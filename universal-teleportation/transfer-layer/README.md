---

# 🚀 WekezaOmniOS: Transfer Layer

The **Transfer Layer** is the circulatory system of the Universal Application Teleportation (UAT) engine. Its primary responsibility is the physical movement of process snapshots between source and target environments.

While **Phase 1** focuses on local node simulation, this module is architected to scale into a robust, distributed transport system supporting SSH, gRPC, and WebRTC.

---

## 🏗️ Purpose & Responsibilities

The Transfer Layer ensures that a captured process state successfully reaches its destination node for restoration.

* **Mobility:** Moves snapshots across different directories, machines, or cloud nodes.
* **Abstraction:** Provides a unified interface for various transport protocols.
* **Orchestration:** Manages the lifecycle of a "transfer job" from source validation to target confirmation.

---

## 📁 Module Structure

| File | Responsibility | Status |
| --- | --- | --- |
| `transfer_manager.py` | The main controller used by the CLI/API to trigger moves. | **Active** |
| `local_transfer.py` | Handles filesystem-level copies for local node simulation. | **Active** |
| `ssh_transfer.py` | A strategic bridge for remote node teleportation. | **Placeholder (Phase 2)** |

---

## 🔄 The Teleportation Flow

This module sits directly in the middle of the teleportation lifecycle:

1. **Capture:** Process state is frozen (State Capture).
2. **Package:** State is bundled into a portable snapshot (Snapshot Engine).
3. **Transfer:** **[Current Module]** Snapshot is moved to the target path/node.
4. **Restore:** Process is rehydrated and resumed (State Reconstruction).

---

## 🛠️ Usage Example (Phase 1)

In the current phase, you can trigger a transfer through the `TransferManager` to simulate moving a process from a development workspace to a testing environment.

```python
from transfer_layer.transfer_manager import TransferManager

# Initialize the manager
tm = TransferManager(snapshot_dir="./snapshots")

# Teleport process 1921 to a target testing folder
tm.send_snapshot(process_id=1921, target_path="./test_environment/restoration_area")

```

---

## 🔗 Integration Roadmap

* **Phase 1 (Local):** Uses `shutil` based copies to verify that snapshots remain intact and portable.
* **Phase 2 (Distributed):** Implementation of `ssh_transfer.py` using `Paramiko` or `SCP` for node-to-node teleportation.
* **Phase 3 (Enterprise):** Integration of **gRPC** and **WebRTC** for high-speed, low-latency "Live Teleportation" between data centers.

---

### ✅ Phase 1: MISSION COMPLETE

With this folder finalized, **WekezaOmniOS** officially has a complete blueprint for Phase 1. Every folder from `api/` to `ui-controls/` is documented, integrated, and ready for code execution.


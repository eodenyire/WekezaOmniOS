# ⚙️ WekezaOmniOS: System Configurations

This module serves as the **Single Source of Truth (SSoT)** for the Universal Application Teleportation (UAT) engine. It decouples the engine logic from the environment settings, allowing for seamless transitions between development, testing, and production phases.

## 🎯 Purpose

* **Centralization:** Manage paths, binaries, and engine flags in one place.
* **Scalability:** Easily switch from "local-node" to "distributed-cluster" by updating a YAML entry.
* **Safety:** Define resource limits (like max snapshot size) to prevent system crashes during a capture.

## 📜 Configuration Inventory

| File | Scope | Key Parameters |
| --- | --- | --- |
| **`system.yaml`** | File System & Nodes | Directories for logs, snapshots, and temp files. |
| **`criu_config.yaml`** | Checkpoint Engine | Paths to CRIU and specific kernel-level flags. |
| **`teleportation.yaml`** | Engine Logic | Restoration modes and global engine defaults. |

---

### 📄 `system.yaml`

This file handles the "Physical Geography" of the engine. It tells the scripts exactly where to put the "Cargo" (Snapshots) and the "Flight Recorder" data (Logs).

```yaml
# WekezaOmniOS: System Paths & Node Identity
# Used by: State Capture, Snapshot Engine, and CLI

snapshot_directory: "./snapshots"
log_directory: "./logs"
temp_directory: "./temp"

# Phase 1: Local Simulation Identity
default_node: "nairobi-local-01"
environment: "development"

```

---

### 📄 `criu_config.yaml`

Since **CRIU** is our engine's "piston," this file ensures it has the right fuel and timing. These settings are critical for handling networking and shell-based processes (like our demo apps).

```yaml
# WekezaOmniOS: CRIU Engine Optimization
# These flags ensure high-fidelity capture of TCP and Unix Sockets.

criu_path: "/usr/sbin/criu"

# Feature Flags
use_shell_job: true      # Allows capturing apps started from a shell
tcp_established: true    # Keep database/API connections alive across the jump
ext_unix_sk: true        # Support for inter-process communication sockets
file_locks: true         # Ensure file integrity during the freeze

```

---

### 📄 `teleportation.yaml`

This is where the "Business Rules" live. It defines the constraints of a "Jump" to ensure that teleportation doesn't become a liability.

```yaml
# WekezaOmniOS: Teleportation Business Logic
# Defines the 'Rules of the Jump'

# Resource Constraints
max_snapshot_size_mb: 500  # Safety limit for Phase 1
compression_level: 6       # Balance between speed and storage size

# Operational Defaults
default_restore_mode: "pause_resume" # Options: pause_resume, live_migration
default_engine: "criu"
enable_logging: true

# Security (Phase 1 Mock)
verify_checksum: true
encrypt_snapshots: false

```

---

### 🔗 The Integration Handoff

These configs act as the glue for the entire Phase 1 pipeline:

1. **State Capture** reads `criu_config.yaml` to know which flags to pass to the kernel.
2. **Snapshot Engine** reads `system.yaml` to find the correct folder to save the `.tar.gz`.
3. **CLI/UI** reads `teleportation.yaml` to set the default behavior for your "Right-Click Teleport" action.

---

### ✅ Configurations: ARCHITECTURE LOCKED

The engine now has its "Rules of Engagement." Everything is standardized, observable, and ready for deployment.

---

# ⌨️ WekezaOmniOS CLI Interface

The **WekezaOmniOS CLI** is the primary developer-facing control interface for the Universal Application Teleportation (UAT) engine. Designed to be "command-line first," it mirrors the workflow of tools like Docker and Kubernetes, allowing for seamless process manipulation via the terminal.

In **Phase 1**, this CLI acts as a modular wrapper that validates user input and coordinates with the underlying engine modules (State Capture, Snapshot Engine, and State Reconstruction).

---

## 🚀 Features

* **Process Capture:** Freeze a running process and prepare it for teleportation.
* **Snapshot Management:** Create portable, named snapshots of captured process states.
* **Process Restoration:** Rehydrate and resume processes from existing snapshots.
* **Engine Telemetry:** Query the status of the teleportation engine (Mocked in Phase 1).

---

## 🛠️ Usage

The CLI is invoked via the `teleport.py` entry point.

### 1. Capture a Process

Freeze a local process using its Process ID (PID).

```bash
python teleport.py capture 1921

```

### 2. Create a Snapshot

Generate a portable state file from a captured process.

```bash
# Basic snapshot
python teleport.py snapshot 1921

# Named snapshot
python teleport.py snapshot 1921 --name "production-hotfix-v1"

```

### 3. Restore a Process

Resume execution from a saved snapshot.

```bash
python teleport.py restore "production-hotfix-v1"

```

### 4. Check Status

Verify the health of the local teleportation engine.

```bash
python teleport.py status

```

---

## 📁 Folder Structure

```text
cli/
├── teleport.py    # Main entry point; parses arguments and delegates logic.
├── commands.py    # Execution layer; contains logic for each CLI command.
├── utils.py       # Helper functions (e.g., PID validation, logging).
├── PLAN.md        # Detailed roadmap for CLI evolution.
└── README.md      # This documentation.

```

---

## 🏗️ Design Philosophy

* **Modular Delegation:** `teleport.py` is kept thin. All command logic is handled in `commands.py` to allow for easy expansion as new engine capabilities are added.
* **Validation First:** Input (like PIDs and filenames) is validated in `utils.py` before hitting the engine to prevent system-level errors.
* **API Parity:** The CLI is designed to eventually serve as a wrapper for the `WekezaOmniOS API`, ensuring a consistent experience whether interacting locally or over a network.

---

## 🔗 Integration Roadmap

As we move from **Phase 1 (Mock)** to **Phase 2 (Active Engine)**, the print statements in `commands.py` will be replaced with direct calls to:

1. **State Capture:** `capture_manager.checkpoint(pid)`
2. **Snapshot Engine:** `snapshot_builder.export(pid, name)`
3. **State Reconstruction:** `restore_manager.rehydrate(name)`

---

Would you like me to move on to designing the **`state-capture/`** directory, including the initial logic for integrating **CRIU**?

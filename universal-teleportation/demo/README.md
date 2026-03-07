# 🎮 WekezaOmniOS Demo Applications

This folder contains the official test-bed applications for the **Universal Application Teleportation (UAT)** engine. These apps are designed to be "Teleport-Ready"—meaning they maintain a clear, observable state that makes it easy to verify if a "jump" was successful.

### ⚖️ The "Guinea Pig" Philosophy

In Phase 1, we don't test on production. We use these demo apps to verify:

1. **State Persistence:** Does the counter resume at the correct number?
2. **File Integrity:** Does the background log continue appending without corruption?
3. **Process Continuity:** Does the PID handover happen without the application crashing?

---

## 📦 Contents

| File | Category | Test Case |
| --- | --- | --- |
| **`demo_app.py`** | Console App | Simple long-running loop to test **CPU state** and **Memory** capture. |
| **`demo_server.py`** | Background Service | Simulates a worker with persistent logging to test **File Handle** restoration. |

---

## 🚀 Usage Instructions

### 1. Running the Counter (`demo_app.py`)

This is your go-to for quick "Capture ⮕ Restore" cycles.

```bash
python3 demo/demo_app.py

```

* **Observable Output:** `[demo_app] WekezaOmniOS Demo Running | Tick X`
* **Verification:** If you capture the process at **Tick 10** and restore it, it must resume at **Tick 11**.

### 2. Running the Background Service (`demo_server.py`)

Use this to test how the engine handles applications that don't have a direct UI.

```bash
python3 demo/demo_server.py

```

* **Observable Output:** Writes to `demo_server.log`.
* **Verification:** Check the log file post-teleportation to ensure the timestamp sequence is continuous.

---

## 🔗 Integration with UAT Engine

These apps are designed to work seamlessly with the **`scripts/run_demo.sh`** utility. When launched via that script, their PIDs are automatically saved to the `temp/` folder, allowing the **Capture Manager** to find them instantly.

> **Note:** These apps are intentionally lightweight to ensure that Phase 1 testing remains fast and does not require massive memory dumps during development.

---

### ✅ Demo Module: DOCUMENTATION LOCKED

The stage is set. We have our targets defined.

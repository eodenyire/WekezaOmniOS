# 🎮 WekezaOmniOS: UI Controls

The **UI Controls** module provides the interaction layer for the Universal Application Teleportation (UAT) engine. It bridges the gap between complex system-level operations and the end-user by providing a visual (or semi-visual) way to manage process migration across the Wekeza ecosystem.

### 🎯 Purpose

* **Process Discovery:** Provides a scannable list of "Teleportable" applications.
* **Orchestration Control:** Simplifies the multi-step process (Capture ⮕ Snapshot ⮕ Restore) into a single user action.
* **Environment Selection:** Offers a curated list of target environments, from local Ubuntu nodes to remote Android or Cloud instances.
* **Observability:** Provides immediate visual feedback on the success or failure of a "Jump."

---

## 🛠️ Key UI Features

### 1. The Selectable Process List

The UI identifies running processes (starting with our Phase 1 `demo_app.py`) and displays their health status, memory usage, and current node location.

### 2. The "Right-Click" Teleport Menu

Inspired by modern desktop environments, this feature simulates a context menu that allows a user to right-click a process and select **"Teleport To..."**.

**Target Options:**

* 🪟 **Windows Node** (via `windows_adapter`)
* 🐧 **Ubuntu Node** (via `linux_adapter`)
* 🤖 **Android Mobile** (via `android_adapter`)
* ☁️ **Cloud Cluster** (via `transfer_layer`)

---

## 📂 Module Breakdown

| File | Responsibility |
| --- | --- |
| **`ui.py`** | The main entry point. In Phase 1, this is a **Console-based GUI** that simulates the selection and triggering of engine commands. |
| **`README.md`** | Documentation of the UI interaction contract and Phase 2 GUI roadmap. |

---

## 🔄 Integration Workflow

The UI acts as the trigger for the entire UAT pipeline:

1. **Selection:** User picks a PID from the `ui.py` list.
2. **Targeting:** User selects the destination (e.g., "Android").
3. **Execution:** The UI calls the `CaptureManager`, which triggers the `SnapshotEngine`.
4. **Reporting:** Success/Failure messages are piped from `logs/teleport.log` back to the UI for user feedback.

---

## 🚀 Phase 2 Roadmap: From CLI to GUI

* **Phase 1:** Interactive Python Console Menu.
* **Phase 2:** Lightweight **PyQt5** or **Tkinter** dashboard for real-time process dragging-and-dropping.
* **Phase 3:** Integration into the **Wekeza Bank Executive Dashboard** for cross-device application "handoffs" (e.g., Mac to iPhone).

---

### ✅ UI Module: MISSION COMPLETE

We have defined the user's primary interface. The engine is no longer just a set of scripts; it is now a **Tool**.

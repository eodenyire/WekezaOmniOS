# 🌉 WekezaOmniOS: Runtime Adapters

The **Runtime Adapters** module provides the abstraction layer necessary for true cross-platform teleportation. In Phase 1, we focus on mocking these translations to establish the architectural "hooks," preparing the engine for the complex system-call translations of Phase 2.

### 🎯 Purpose

* **Cross-OS Compatibility:** Translate process state, file paths, and system calls between different kernel expectations.
* **Environment Mapping:** Convert Linux-style signals (SIGTERM) into Windows-style events or Android-specific intents.
* **Path Normalization:** Ensure `/home/user/app` (Linux) is correctly interpreted as `C:\Users\User\app` (Windows) during restoration.

---

## 📂 Module Structure

To keep the engine modular, every supported OS has its own dedicated adapter:

| File | Responsibility |
| --- | --- |
| **`linux_adapter.py`** | Handles POSIX signals, `/proc` filesystem mapping, and Linux system calls. |
| **`windows_adapter.py`** | Maps Windows Registry keys, DLL paths, and handle management. |
| **`android_adapter.py`** | Adjusts for the Dalvik/ART runtime and Android's unique permission model. |

---

## 🔄 Teleportation Translation Logic

The adapters act as a "Post-Processor" during the **State Reconstruction** phase.

1. **Ingress:** The engine provides the raw snapshot.
2. **Detection:** The adapter identifies the target OS.
3. **Translation:** The adapter modifies environment variables, file handles, and memory pointers to match the target architecture.
4. **Egress:** A "target-ready" state is handed to the kernel for execution.

---

## 🛠️ Usage Example (Internal API)

This allows the CLI or UI to trigger a teleportation move regardless of the source/target hardware.

```python
from runtime_adapters.linux_adapter import LinuxAdapter
from runtime_adapters.windows_adapter import WindowsAdapter

# Scenario: Teleporting to a Windows Node
adapter = WindowsAdapter()

# Translate the captured Linux snapshot into a Windows-compatible state
translated_snapshot = adapter.translate_process_state(linux_snapshot)

```

---

## 🔗 Integration Plan

This module is the final "sanity check" in the Universal Application Teleportation (UAT) pipeline:

> **State Capture** ⮕ **Snapshot Engine** ⮕ **State Reconstruction** ⮕ **Runtime Adapters**

* **Phase 1:** Mocking the translation logic to prove the API and folder structure.
* **Phase 2:** Implementing real-time system call emulation and instruction set translation (e.g., x86 to ARM).

---

### ✅ Module Status: ARCHITECTURE LOCKED

The folder structure for `runtime-adapters/` is now officially ready for development.

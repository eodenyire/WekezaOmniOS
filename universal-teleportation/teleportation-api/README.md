---

# 🚀 WekezaOmniOS: Teleportation API

The **Teleportation API** is the programmatic gateway to the Universal Application Teleportation (UAT) engine. It provides the high-level orchestration required to move running processes across the Wekeza Bank ecosystem.

By exposing the engine's capabilities via REST endpoints, this module allows for seamless integration with the CLI, the circular UI selector, and automated DevOps pipelines.

---

## 🎯 Purpose & Responsibilities

This module acts as the "Brain" of the operation, coordinating the handoffs between the various engine subsystems.

* **Endpoint Exposure:** Provides a clean interface for process capture, snapshotting, and restoration.
* **External Control:** Enables the CLI and UI to trigger complex systems-level operations via standard HTTP/JSON.
* **Input Validation:** Uses Pydantic models to ensure every teleportation request is well-formed before execution.
* **Orchestration:** Manages the Phase 1 workflow by sequencing calls to `state-capture`, `snapshot-engine`, and `state-reconstruction`.

---

## 📂 Module Structure

| File | Responsibility |
| --- | --- |
| `server.py` | The main entry point; handles the FastAPI application lifecycle. |
| `routes.py` | Defines the API endpoints and maps them to engine logic. |
| `models.py` | Contains the data schemas (Request/Response) for validation. |

---

## 📡 API Reference

### **POST** `/engine/teleport`

Initiates a teleportation sequence for a running process.

**Request Body:**

```json
{
  "process_id": 1921,
  "source_env": "ubuntu-dev",
  "target_env": "windows-test"
}

```

**Successful Response:**

```json
{
  "status": "success",
  "message": "Process 1921 teleportation from ubuntu-dev to windows-test has been initiated."
}

```

---

## 🛠️ Phase 1 Usage

To boot the API control plane during development:

1. **Start the Server:**
```bash
python server.py

```


2. **Access Documentation:**
FastAPI automatically generates interactive docs at: `http://localhost:8000/docs`
3. **Local Workflow:**
In Phase 1, a call to this API prints orchestration details and prepares the internal hooks to trigger:
* `state-capture.capture_manager`
* `snapshot-engine.snapshot_builder`
* `state-reconstruction.restore_manager`



---

## 🔗 Integration Plan

The API sits at the center of the **WekezaOmniOS** data flow:

```text
CLI / UI ⮕ Teleportation API ⮕ State Capture ⮕ Snapshot Engine ⮕ Transfer Layer ⮕ State Reconstruction

```

* **Phase 1:** Focuses on orchestrating the local loop using mock/initial logic.
* **Phase 2:** Will expand to include real-time status monitoring, multi-node orchestration, and gRPC support for high-speed state streaming.

---

### ✅ Mission Accomplished: Phase 1 Architecture


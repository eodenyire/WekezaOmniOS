---

# 🌌 WekezaOmniOS: Universal Teleportation API

This module provides the RESTful control interface for the **Universal Application Teleportation (UAT)** engine. It allows developers and system administrators to migrate running processes across heterogeneous environments with minimal downtime.

The API acts as the primary orchestrator for:

* **Capturing** active process states.
* **Generating** portable process snapshots.
* **Restoring** execution on target nodes.
* **Monitoring** real-time teleportation telemetry.

> **Phase 1 Note:** The API is currently optimized as a local control interface. Future iterations will evolve this into a distributed, multi-node teleportation control plane.

---

## 🏗️ Architecture

The API serves as a lightweight abstraction layer, delegating the heavy lifting of state manipulation to the underlying engine.

```text
Client / CLI / UI
       ↓
Teleportation API (FastAPI/Uvicorn)
       ↓
Teleportation Engine
       ↓
State Capture ↔ Snapshot Engine ↔ State Reconstruction

```

---

## 🚀 Endpoints

### Orchestration & Control

| Method | Endpoint | Description |
| --- | --- | --- |
| **POST** | `/teleport` | High-level migration between environments |
| **POST** | `/capture` | Trigger state capture of a specific PID |
| **POST** | `/snapshot` | Generate a filesystem snapshot from captured state |
| **POST** | `/restore` | Rehydrate and resume a process from a snapshot |
| **GET** | `/status` | Retrieve current engine and migration status |

---

## 🛠️ Usage Examples

### 1. Full Teleportation (Environment to Environment)

Move a process from a development container to a testing environment in one call.

**Request:** `POST /teleport`

```json
{
  "process_id": 1921,
  "source_env": "ubuntu-dev",
  "target_env": "windows-test"
}

```

### 2. Manual Process Capture

Initiate a granular capture of a local process.

**Request:** `POST /capture`

```json
{
  "pid": 2451
}

```

**Response:**

```json
{
  "status": "capturing",
  "pid": 2451,
  "timestamp": "2026-03-07T19:21:00Z"
}

```

---

## 💻 Getting Started

### Running the API

The API is built on FastAPI and uses Uvicorn as the ASGI server. Start the development server with:

```bash
uvicorn server:app --reload

```

### Accessing Documentation

Once the server is running, you can access the interactive API playground:

* **Local Server:** [http://localhost:8000](https://www.google.com/search?q=http://localhost:8000)
* **Interactive Swagger UI:** [http://localhost:8000/docs](https://www.google.com/search?q=http://localhost:8000/docs)
* **Alternative ReDoc:** [http://localhost:8000/redoc](https://www.google.com/search?q=http://localhost:8000/redoc)

---

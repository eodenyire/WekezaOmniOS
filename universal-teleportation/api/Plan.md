Perfect approach. Building **folder by folder with full documentation and architecture** is exactly how serious systems projects evolve. We’ll start with:

```
WekezaOmniOS/
└── universal-teleportation/
    └── api/
```

The **API module** will act as the **control plane for teleportation operations**. Even though Phase 1 is local checkpointing, the API prepares the system for **future distributed teleportation (Phase 2+)**.

---

# 📁 Folder: `api/`

Purpose:
Provide a **programmatic interface** to control teleportation actions like:

* capture process
* create snapshot
* restore process
* query teleportation status

Architecture style:

```
Client
   ↓
REST API
   ↓
Teleportation Engine
   ↓
Capture / Snapshot / Restore modules
```

We’ll implement the API using **FastAPI**.

---

# 📄 `api/README.md`

Create:

```md
# Universal Teleportation API

This module exposes REST endpoints used to control the Universal Application Teleportation (UAT) engine.

The API acts as the control interface for:

- capturing running processes
- generating process snapshots
- restoring processes from snapshots
- monitoring teleportation status

The API is intentionally lightweight so it can operate as a local control interface in Phase 1 and evolve into a distributed teleportation control plane in later phases.

---

## Architecture

```

Client / CLI / UI
↓
Teleportation API
↓
Teleportation Engine
↓
State Capture
Snapshot Engine
State Reconstruction

```

The API does not implement teleportation logic directly. Instead, it delegates tasks to internal modules.

---

## Endpoints

| Endpoint | Description |
|--------|--------|
| POST /capture | Capture a running process |
| POST /snapshot | Create snapshot |
| POST /restore | Restore process |
| GET /status | Get teleportation status |

---

## Example Request

```

POST /capture

```

Body:

```

{
"pid": 2451
}

```

Response:

```

{
"status": "capturing",
"pid": 2451
}

```

---

## Running the API

```

uvicorn server:app --reload

```

Default server:

```

[http://localhost:8000](http://localhost:8000)

```

API documentation will be automatically available at:

```

[http://localhost:8000/docs](http://localhost:8000/docs)

```

---

## Future Extensions

In later phases, this API will support:

- node-to-node teleportation
- distributed snapshot storage
- cluster orchestration
- remote teleportation requests
```

---

# 📄 `models.py`

Defines **data structures used by the API**.

```python
from pydantic import BaseModel
from typing import Optional


class CaptureRequest(BaseModel):
    pid: int


class SnapshotRequest(BaseModel):
    pid: int
    snapshot_name: Optional[str] = None


class RestoreRequest(BaseModel):
    snapshot_name: str


class TeleportStatus(BaseModel):
    status: str
    message: Optional[str] = None
```

Why this matters:

* structured API contracts
* automatic validation
* OpenAPI documentation generation

---

# 📄 `routes.py`

Defines **all API endpoints**.

```python
from fastapi import APIRouter
from models import CaptureRequest, SnapshotRequest, RestoreRequest

router = APIRouter()


@router.post("/capture")
def capture_process(request: CaptureRequest):
    return {
        "status": "capturing",
        "pid": request.pid
    }


@router.post("/snapshot")
def create_snapshot(request: SnapshotRequest):
    return {
        "status": "snapshot_created",
        "pid": request.pid,
        "snapshot": request.snapshot_name
    }


@router.post("/restore")
def restore_process(request: RestoreRequest):
    return {
        "status": "restoring",
        "snapshot": request.snapshot_name
    }


@router.get("/status")
def status():
    return {
        "status": "teleportation_engine_running"
    }
```

Right now these endpoints return **mock responses**.

Later they will call:

```
state-capture/
snapshot-engine/
state-reconstruction/
```

---

# 📄 `server.py`

Main API entry point.

```python
from fastapi import FastAPI
from routes import router

app = FastAPI(
    title="WekezaOmniOS Universal Teleportation API",
    description="API for controlling Universal Application Teleportation",
    version="0.1"
)

app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "WekezaOmniOS Universal Teleportation API",
        "status": "running"
    }
```

Run server:

```
uvicorn server:app --reload
```

Open:

```
http://127.0.0.1:8000/docs
```

FastAPI will auto-generate an **interactive API console**.

---

# 📂 Final `api/` Folder Structure

```
api/

README.md
server.py
routes.py
models.py
```

---

# 🔗 How This Integrates With Teleportation Engine

Later integration flow:

```
POST /capture
      ↓
routes.py
      ↓
state_capture.capture_manager()
      ↓
CRIU checkpoint
```

Snapshot flow:

```
POST /snapshot
      ↓
snapshot_engine.snapshot_builder()
```

Restore flow:

```
POST /restore
      ↓
state_reconstruction.restore_manager()
```

---

# ✅ What We Achieved

We now have:

* teleportation control API
* typed request models
* endpoint routing
* architecture documentation
* integration design

Even before writing the engine, we already have a **clean control plane**.

---

# 🚀 Next Folder

Next we should design the **most critical module in Phase 1**:

```
universal-teleportation/state-capture/
```

This is where **real teleportation begins** because it handles **process checkpointing using CRIU**.

That folder will contain the **first real systems-level logic** in the project.

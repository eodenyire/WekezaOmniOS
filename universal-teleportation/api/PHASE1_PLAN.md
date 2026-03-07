Great! Now we are in the **`teleportation-api/` folder**, which provides **the interface for controlling teleportation programmatically**. This module allows developers or external systems to trigger **capture, snapshot, and restore operations** through **HTTP requests** (or later gRPC).

This makes **Universal Application Teleportation (UAT)** accessible from **CLI, UI, or automated pipelines**.

---

# 📁 Folder: `teleportation-api/`

Purpose:

* Expose **teleportation operations as API endpoints**
* Allow external control of **process capture, snapshot, and restore**
* Enable integration with **UI and CLI**
* Provide **JSON-based inputs/outputs** for automation

Responsibilities:

* `server.py` — main API server entrypoint
* `routes.py` — define endpoints (`/teleport`, `/capture`, `/restore`)
* `models.py` — define request/response schemas for validation

---

# 📄 `README.md`

````md id="api1x7k"
# WekezaOmniOS Teleportation API

This module exposes HTTP endpoints to control Universal Application Teleportation (UAT).

## Endpoints

### POST /teleport

Teleport a running process between environments.

**Request Body:**
```json
{
  "process_id": 1921,
  "source_env": "ubuntu-dev",
  "target_env": "windows-test"
}
````

**Response:**

```json
{
  "status": "success",
  "message": "Process 1921 teleportation started."
}
```

## Phase 1 Usage

* Run `server.py`
* Send POST requests to `/teleport`
* API will internally trigger:

  * `state-capture.capture_manager`
  * `snapshot-engine.snapshot_builder`
  * `state-reconstruction.restore_manager`

````

---

# 📄 `models.py`

```python id="api2x9v"
from pydantic import BaseModel

class TeleportRequest(BaseModel):
    process_id: int
    source_env: str
    target_env: str

class TeleportResponse(BaseModel):
    status: str
    message: str
````

---

# 📄 `routes.py`

```python id="api3x8d"
from fastapi import APIRouter
from models import TeleportRequest, TeleportResponse

router = APIRouter()

@router.post("/teleport", response_model=TeleportResponse)
def teleport_process(request: TeleportRequest):
    # Placeholder logic for Phase 1
    process_id = request.process_id
    source_env = request.source_env
    target_env = request.target_env
    print(f"[Teleport API] Teleport request: PID={process_id}, {source_env} → {target_env}")
    # TODO: integrate with capture → snapshot → restore
    return TeleportResponse(status="success", message=f"Process {process_id} teleportation started.")
```

---

# 📄 `server.py`

```python id="api4x7q"
import uvicorn
from fastapi import FastAPI
from routes import router

app = FastAPI(title="WekezaOmniOS Teleportation API")

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

# 🔗 Integration Plan

```text id="api5x4f"
CLI / UI → teleportation-api → state-capture → snapshot-engine → snapshot/ → state-reconstruction
```

* CLI/UI calls POST `/teleport`
* API validates input via `models.py`
* Triggers capture → snapshot → restore workflow
* Phase 1: placeholder logic, prints info and logs
* Phase 2: full integration with runtime adapters and cross-OS teleportation

---

# 📂 Folder Structure

```text id="api6x9h"
teleportation-api/
    README.md
    models.py
    routes.py
    server.py
```

---

✅ **Next Step:**

After `teleportation-api/`, the next **folder is `tests/`**, where we will **design unit tests and integration tests** for teleportation Phase 1.

Do you want me to **design `tests/` next with initial test files and README**?

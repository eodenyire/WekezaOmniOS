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

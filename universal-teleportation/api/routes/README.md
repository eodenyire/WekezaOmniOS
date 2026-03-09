# API Routes

This folder contains FastAPI router modules grouped by surface area.

## Purpose

Route modules define transport-level behavior:

- endpoint paths and tags
- request/response schema binding
- request parsing and validation handoff
- mapping controller results to API responses

## Files

- `teleportation_routes.py`
- `developer_routes.py`
- `ai_routes.py`
- `terminal_routes.py`
- `__init__.py`

## Route Groups

### `teleportation_routes.py`

Core teleportation and cluster APIs, including:

- `/status`
- `/capture`, `/snapshot`, `/restore`
- `/teleport`, `/teleport/remote`, `/teleport/container`
- cluster node management endpoints
- `/console` UI endpoint

### `developer_routes.py`

Developer IDE APIs and UI bridge:

- `/developer` UI page
- file and folder operations
- multi-language run/compile execution endpoint
- deploy handoff endpoint that produces production and console bridge links

### `ai_routes.py`

Assistant chat endpoint(s) used by integrated IDE flows.

### `terminal_routes.py`

WebSocket terminal endpoint for browser-integrated shell sessions.

## Design Notes

- Route modules import schemas from `api/schemas/` and controllers from `api/controllers/`.
- Top-level files like `api/routes.py` are compatibility wrappers and should stay lightweight.
- UI HTML assets are served from `api/ui/`.

## Extension Guidance

For a new route set:

1. create a dedicated module in this folder
2. expose a `router = APIRouter(...)`
3. include it in `api/server.py`
4. if needed for compatibility, re-export from top-level wrapper files in `api/`

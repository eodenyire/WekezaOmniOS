# Cloud Desktop Model

The Cloud Desktop Model is the third OmniOS implementation track. It treats
the desktop as a remotely orchestrated service: compute, storage, API management,
and browser delivery are all handled through distributed cloud components.

## Architecture

```
cloud-desktop-model/
├── api-gateway/            # FastAPI control plane + auth + routes
│   ├── server.py           # FastAPI application entry-point
│   ├── schemas/models.py   # Pydantic request / response schemas
│   ├── routes/
│   │   ├── auth_routes.py         # POST /auth/register, /login, /logout
│   │   ├── os_launcher_routes.py  # POST /sessions/launch, DELETE /sessions/{id}
│   │   ├── workspace_routes.py    # CRUD /workspaces, /clone, /snapshot
│   │   └── cluster_routes.py     # /cluster/nodes, /cluster/health
│   ├── controllers/
│   │   ├── auth_controller.py
│   │   ├── os_launcher_controller.py
│   │   └── workspace_controller.py
│   ├── middleware/auth_middleware.py  # Bearer-token validation
│   └── ui/dashboard.html              # Full web dashboard SPA
│
├── compute-nodes/          # Node implementations (Linux / Windows / Android)
│   ├── node_base.py
│   ├── linux_node.py
│   ├── windows_node.py
│   ├── android_emulator_node.py
│   └── node_pool.py
│
├── control-plane/          # Orchestration brain
│   ├── control_plane.py    # Top-level façade
│   ├── cluster_scheduler.py
│   ├── resource_allocator.py
│   └── node_monitor.py
│
├── storage-system/         # User data and object storage
│   ├── storage_manager.py
│   ├── object_storage.py   # MinIO-inspired local store
│   ├── distributed_fs.py   # Ceph-inspired distributed FS
│   └── user_data_manager.py
│
├── workspace-manager/      # Developer environment lifecycle
│   ├── workspace_manager.py   # start / clone / snapshot
│   └── workspace_registry.py
│
├── web-platform/           # Web-tier entry-point
│   └── app.py
│
├── start_server.py         # Run the full stack
└── requirements.txt
```

## Quick Start

```bash
cd cloud-desktop-model
pip install -r requirements.txt
python start_server.py
```

The API Gateway will start on **port 8080**.

| URL | Description |
|-----|-------------|
| http://localhost:8080/docs | Swagger interactive API docs |
| http://localhost:8080/redoc | ReDoc API docs |
| http://localhost:8080/dashboard | Web dashboard (login + full UI) |

## Typical Workflow

1. **Register + login** via `/auth/register` and `/auth/login` to get a bearer token.
2. **Register compute nodes** via `POST /cluster/nodes` (linux / windows / android-emulator).
3. **Launch an OS session** via `POST /sessions/launch` — the scheduler picks the best node.
4. **Create a workspace** via `POST /workspaces` — wraps a session with persistent metadata.
5. **Clone or snapshot** a workspace via `/workspaces/clone` and `/workspaces/snapshot`.
6. **Monitor** the cluster with `GET /cluster/health` and `GET /cluster/resources`.

## Supported OS Profiles

| Profile | Node Type |
|---------|-----------|
| `ubuntu-22.04`, `debian-12`, `fedora-39`, `arch-latest` | linux |
| `windows-11`, `windows-10`, `windows-server-2022` | windows |
| `android-14`, `android-13`, `android-12`, `android-11` | android-emulator |

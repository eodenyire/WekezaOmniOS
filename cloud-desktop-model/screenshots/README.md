# Cloud Desktop Model — End-to-End Journey Screenshots

These screenshots were captured by running the end-to-end journey script:

```bash
cd cloud-desktop-model
python e2e_journey.py
```

Each PNG is named `<step_number>_<description>.png` and documents a specific
step in the full system journey.

---

## Step-by-step Walkthrough

| # | Screenshot | Description |
|---|-----------|-------------|
| 01 | `01_api_gateway_health_check.png` | API Gateway `/status` endpoint — confirms the server is online with resource usage |
| 02 | `02_dashboard_login_page.png` | Dashboard login screen — entry point for the Cloud Desktop UI |
| 03 | `03_register_form_filled.png` | Registration form filled in for user *alice* |
| 04 | `04_register_user_success.png` | Successful account creation confirmation |
| 05 | `05_login_credentials_filled.png` | Login credentials entered |
| 06 | `06_dashboard_overview_post_login.png` | Dashboard overview after login — cluster stats, API status, node health |
| 07 | `07_cluster_register_linux_node_form.png` | Cluster tab — Linux node registration form filled in |
| 08 | `08_cluster_linux_node_registered.png` | Linux compute node `linux-node-01` registered successfully |
| 09 | `09_cluster_windows_node_registered_api.png` | Windows node `windows-node-01` registered via API |
| 10 | `10_cluster_all_nodes_listed.png` | All three nodes (Linux, Windows, Android Emulator) listed in the cluster |
| 11 | `11_sessions_launch_ubuntu_form.png` | Sessions tab — Ubuntu 22.04 OS session launch form |
| 12 | `12_sessions_ubuntu_session_launched.png` | Ubuntu session launched successfully with session ID and connect URL |
| 13 | `13_sessions_windows11_session_launched.png` | Windows 11 session also launched (via API), sessions list refreshed |
| 14 | `14_sessions_active_list.png` | Active sessions table — both Ubuntu and Windows 11 sessions |
| 15 | `15_session_detail_json.png` | JSON detail view of a single session (session ID, node, connect URL) |
| 16 | `16_workspaces_create_form.png` | Workspaces tab — create workspace form for *my-dev-env* |
| 17 | `17_workspaces_created.png` | Workspace created, confirmation message with workspace ID |
| 18 | `18_workspaces_list.png` | Workspaces list showing the newly created workspace |
| 19 | `19_workspace_detail_after_snapshot.png` | Workspace JSON detail after taking snapshot `snap-v1` |
| 20 | `20_workspace_clone_detail.png` | Cloned workspace JSON detail (`my-dev-env-clone`) |
| 21 | `21_workspaces_list_after_clone.png` | Workspaces list showing original + clone |
| 22 | `22_cluster_health_nodes_view.png` | Cluster tab with all nodes and their live health status |
| 23 | `23_devtools_resource_usage_ready.png` | Dev Tools — API Explorer ready to call `/cluster/resources` |
| 24 | `24_devtools_resource_usage_result.png` | Dev Tools — resource usage JSON response (CPU, RAM totals & usage) |
| 25 | `25_devtools_status_result.png` | Dev Tools — `/status` JSON response showing active sessions & nodes |
| 26 | `26_sessions_before_terminate.png` | Sessions tab before terminating the first session |
| 27 | `27_sessions_after_terminate.png` | Sessions tab after terminating — session removed from active list |
| 28 | `28_swagger_ui_docs.png` | Swagger interactive API docs at `/docs` |
| 29 | `29_redoc_ui_docs.png` | ReDoc API reference at `/redoc` |
| 30 | `30_dashboard_final_overview.png` | Final dashboard overview — updated cluster metrics after full journey |

---

## Journey Summary

The end-to-end journey exercises the complete Cloud Desktop Model stack:

1. **Auth** — register a user, login, obtain a bearer token
2. **Cluster** — register Linux, Windows, and Android Emulator compute nodes
3. **Sessions** — launch Ubuntu 22.04 and Windows 11 OS sessions
4. **Workspaces** — create, snapshot, and clone a developer workspace
5. **Monitoring** — inspect cluster health, resource usage, and individual session detail
6. **Teardown** — terminate an OS session
7. **API Docs** — Swagger UI and ReDoc reference

To regenerate all screenshots, run:

```bash
cd cloud-desktop-model
python e2e_journey.py
```

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
| 06 | `06_welcome_screen_os_picker.png` | **Welcome screen** shown after sign-in — 9 OS icon cards (Ubuntu, Debian, Fedora, Arch, Windows 10/11/Server, Android 13/14) |
| 07 | `07_sessions_tab_after_ubuntu_pick.png` | Sessions tab after clicking the Ubuntu card on the welcome screen — Ubuntu session launched automatically |
| 08 | `08_dashboard_overview_post_login.png` | Dashboard overview — cluster stats, API status, and node health |
| 09 | `09_cluster_register_linux_node_form.png` | Cluster tab — Linux node registration form filled in |
| 10 | `10_cluster_linux_node_registered.png` | Linux compute node `linux-node-01` registered successfully |
| 11 | `11_cluster_windows_node_registered_api.png` | Windows node `windows-node-01` registered via API |
| 12 | `12_cluster_all_nodes_listed.png` | All nodes (Linux, Windows, Android Emulator) listed in the cluster |
| 13 | `13_sessions_launch_ubuntu_form.png` | Sessions tab — Ubuntu 22.04 OS session launch form |
| 14 | `14_sessions_ubuntu_session_launched.png` | Ubuntu session launched successfully with session ID and connect URL |
| 15 | `15_sessions_windows11_session_launched.png` | Windows 11 session also launched (via API), sessions list refreshed |
| 16 | `16_sessions_active_list.png` | Active sessions table — all running sessions |
| 17 | `17_session_detail_json.png` | JSON detail view of a single session (session ID, node, connect URL) |
| 18 | `18_workspaces_create_form.png` | Workspaces tab — create workspace form for *my-dev-env* |
| 19 | `19_workspaces_created.png` | Workspace created, confirmation message with workspace ID |
| 20 | `20_workspaces_list.png` | Workspaces list showing the newly created workspace |
| 21 | `21_workspace_detail_after_snapshot.png` | Workspace JSON detail after taking snapshot `snap-v1` |
| 22 | `22_workspace_clone_detail.png` | Cloned workspace JSON detail (`my-dev-env-clone`) |
| 23 | `23_workspaces_list_after_clone.png` | Workspaces list showing original + clone |
| 24 | `24_cluster_health_nodes_view.png` | Cluster tab with all nodes and their live health status |
| 25 | `25_devtools_resource_usage_ready.png` | Dev Tools — API Explorer ready to call `/cluster/resources` |
| 26 | `26_devtools_resource_usage_result.png` | Dev Tools — resource usage JSON response (CPU, RAM totals & usage) |
| 27 | `27_devtools_status_result.png` | Dev Tools — `/status` JSON response showing active sessions & nodes |
| 28 | `28_sessions_before_terminate.png` | Sessions tab before terminating the first session |
| 29 | `29_sessions_after_terminate.png` | Sessions tab after terminating — session removed from active list |
| 30 | `30_swagger_ui_docs.png` | Swagger interactive API docs at `/docs` |
| 31 | `31_redoc_ui_docs.png` | ReDoc API reference at `/redoc` |
| 32 | `32_dashboard_final_overview.png` | Final dashboard overview — updated cluster metrics after full journey |

---

## Journey Summary

The end-to-end journey exercises the complete Cloud Desktop Model stack:

1. **Auth** — register a user, login, obtain a bearer token
2. **Welcome screen** — OS-picker with icon cards; click Ubuntu to launch a session directly
3. **Cluster** — register Linux, Windows, and Android Emulator compute nodes
4. **Sessions** — launch Ubuntu 22.04 and Windows 11 OS sessions
5. **Workspaces** — create, snapshot, and clone a developer workspace
6. **Monitoring** — inspect cluster health, resource usage, and individual session detail
7. **Teardown** — terminate an OS session
8. **API Docs** — Swagger UI and ReDoc reference

To regenerate all screenshots, run:

```bash
cd cloud-desktop-model
python e2e_journey.py
```

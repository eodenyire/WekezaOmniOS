"""
WekezaOmniOS Cloud Desktop Model — End-to-End Journey Script
=============================================================

Walks through the complete system journey step by step, taking a browser
screenshot at every meaningful point.  Screenshots are saved to:

    cloud-desktop-model/screenshots/

Steps covered
-------------
 1.  Server start-up — API Gateway health check
 2.  Dashboard login page
 3.  Register a new user
 4.  Login and receive bearer token
 5.  Dashboard overview (post-login)
 6.  Register a Linux compute node
 7.  Register a Windows compute node
 8.  Register an Android Emulator node
 9.  Cluster tab — list registered nodes
10.  Launch an Ubuntu OS session
11.  Launch a Windows 11 OS session
12.  Sessions tab — active sessions
13.  Create a developer workspace
14.  Workspaces tab — list workspaces
15.  Snapshot the workspace
16.  Clone the workspace
17.  Workspaces tab — after clone
18.  Cluster health check
19.  Resource usage summary
20.  Terminate the first OS session
21.  Developer Tools tab — API explorer
22.  Swagger UI (/docs)
23.  ReDoc UI (/redoc)

Usage
-----
    cd cloud-desktop-model
    python e2e_journey.py

The script starts the API server itself, so nothing needs to be running
beforehand.  It tears the server down once all screenshots have been taken.
"""

import os
import sys
import time
import subprocess
import signal
import textwrap
import requests
from pathlib import Path
from playwright.sync_api import sync_playwright, Page

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
_HERE = Path(__file__).parent.resolve()
_SCREENSHOTS = _HERE / "screenshots"
_SCREENSHOTS.mkdir(exist_ok=True)

BASE_URL = "http://127.0.0.1:8080"
TIMEOUT_MS = 15_000  # 15 s network / JS timeout for Playwright

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
_step_counter = [0]


def step(label: str) -> str:
    """Return a zero-padded filename stem and print the step."""
    _step_counter[0] += 1
    slug = label.lower().replace(" ", "_").replace("/", "_").replace("-", "_")
    filename = f"{_step_counter[0]:02d}_{slug}.png"
    print(f"  → [{_step_counter[0]:02d}] {label}")
    return str(_SCREENSHOTS / filename)


def screenshot(page: Page, label: str) -> None:
    """Scroll to top and save a full-page screenshot."""
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(400)
    path = step(label)
    page.screenshot(path=path, full_page=True)
    print(f"       saved: {Path(path).name}")


def wait_for_server(timeout: int = 30) -> None:
    """Poll /status until the server responds (or raise)."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            r = requests.get(f"{BASE_URL}/status", timeout=2)
            if r.status_code == 200:
                return
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(0.5)
    raise RuntimeError("Server did not start within timeout")


def api(method: str, path: str, body: dict = None, token: str = None) -> dict:
    """Thin wrapper around requests for JSON API calls."""
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    url = f"{BASE_URL}{path}"
    fn = getattr(requests, method.lower())
    kwargs = {"headers": headers, "timeout": 10}
    if body is not None:
        kwargs["json"] = body
    r = fn(url, **kwargs)
    try:
        return r.json()
    except Exception:
        return {"_raw": r.text, "_status": r.status_code}


# ---------------------------------------------------------------------------
# Start server
# ---------------------------------------------------------------------------
def start_server() -> subprocess.Popen:
    print("\n[SETUP] Starting Cloud Desktop API server …")
    env = os.environ.copy()
    env["PYTHONPATH"] = str(_HERE)
    proc = subprocess.Popen(
        [sys.executable, str(_HERE / "start_server.py")],
        cwd=str(_HERE),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    wait_for_server(timeout=30)
    print("[SETUP] Server ready.\n")
    return proc


def stop_server(proc: subprocess.Popen) -> None:
    print("\n[TEARDOWN] Stopping server …")
    try:
        proc.send_signal(signal.SIGTERM)
        proc.wait(timeout=5)
    except Exception:
        proc.kill()
    print("[TEARDOWN] Done.")


# ---------------------------------------------------------------------------
# Journey
# ---------------------------------------------------------------------------
def run_journey(page: Page) -> None:
    page.set_default_timeout(TIMEOUT_MS)
    page.set_default_navigation_timeout(TIMEOUT_MS)

    # ------------------------------------------------------------------
    # Step 1 – API health endpoint (raw JSON in browser)
    # ------------------------------------------------------------------
    page.goto(f"{BASE_URL}/status")
    page.wait_for_load_state("networkidle")
    screenshot(page, "api_gateway_health_check")

    # ------------------------------------------------------------------
    # Step 2 – Dashboard login page
    # ------------------------------------------------------------------
    page.goto(f"{BASE_URL}/dashboard")
    page.wait_for_load_state("networkidle")
    page.wait_for_selector("#loginPanel", state="visible")
    screenshot(page, "dashboard_login_page")

    # ------------------------------------------------------------------
    # Step 3 – Show the register form, fill it in
    # ------------------------------------------------------------------
    page.click("text=Register")
    page.wait_for_selector("#regForm", state="visible")
    page.fill("#regUser", "alice")
    page.fill("#regPass", "s3cr3t!!")
    page.fill("#regEmail", "alice@example.com")
    screenshot(page, "register_form_filled")

    # ------------------------------------------------------------------
    # Step 4 – Submit registration
    # ------------------------------------------------------------------
    page.click("text=Create Account")
    page.wait_for_timeout(600)
    screenshot(page, "register_user_success")

    # ------------------------------------------------------------------
    # Step 5 – Fill login credentials
    # ------------------------------------------------------------------
    page.fill("#loginUser", "alice")
    page.fill("#loginPass", "s3cr3t!!")
    screenshot(page, "login_credentials_filled")

    # ------------------------------------------------------------------
    # Step 6 – Sign in → dashboard overview
    # ------------------------------------------------------------------
    page.click("text=Sign In")
    page.wait_for_selector("#appShell", state="visible", timeout=8_000)
    page.wait_for_timeout(800)
    screenshot(page, "dashboard_overview_post_login")

    # ------------------------------------------------------------------
    # Use the REST API directly to get a token for subsequent API steps.
    # The UI already has it in localStorage; we re-fetch for our script.
    # ------------------------------------------------------------------
    token_resp = api("POST", "/auth/login", {"username": "alice", "password": "s3cr3t!!"})
    token = token_resp.get("access_token", "")
    print(f"       token obtained: {token[:16]}…")

    # ------------------------------------------------------------------
    # Step 7 – Navigate to Cluster tab and register a Linux node
    # ------------------------------------------------------------------
    page.click("text=🖧 Cluster")
    page.wait_for_selector("#tabCluster", state="visible")
    page.fill("#nodeId", "linux-node-01")
    page.select_option("#nodeType", "linux")
    page.fill("#nodeAddr", "10.0.0.1")
    page.fill("#nodeCPU", "8")
    page.fill("#nodeRAM", "16")
    screenshot(page, "cluster_register_linux_node_form")

    page.locator("#tabCluster button:has-text('Register')").click()
    page.wait_for_timeout(600)
    screenshot(page, "cluster_linux_node_registered")

    # ------------------------------------------------------------------
    # Step 8 – Register a Windows node (via API, then refresh UI)
    # ------------------------------------------------------------------
    api("POST", "/cluster/nodes", {
        "node_id": "windows-node-01",
        "node_type": "windows",
        "address": "10.0.0.2",
        "cpu_cores": 8,
        "ram_gb": 16,
    }, token=token)
    page.fill("#nodeId", "windows-node-01")
    page.select_option("#nodeType", "windows")
    page.fill("#nodeAddr", "10.0.0.2")
    screenshot(page, "cluster_windows_node_registered_api")

    # ------------------------------------------------------------------
    # Step 9 – Register Android Emulator node (via API)
    # ------------------------------------------------------------------
    api("POST", "/cluster/nodes", {
        "node_id": "android-emu-01",
        "node_type": "android-emulator",
        "address": "10.0.0.3",
        "cpu_cores": 4,
        "ram_gb": 8,
    }, token=token)

    # Refresh node list in the UI
    page.locator("#tabCluster button:has-text('Refresh')").click()
    page.wait_for_timeout(700)
    screenshot(page, "cluster_all_nodes_listed")

    # ------------------------------------------------------------------
    # Step 10 – Launch an Ubuntu OS session (via UI)
    # ------------------------------------------------------------------
    page.click("text=🚀 Sessions")
    page.wait_for_selector("#tabSessions", state="visible")
    page.fill("#sessUser", "alice")
    page.select_option("#sessOS", "ubuntu-22.04")
    page.fill("#sessCPU", "2")
    page.fill("#sessRAM", "4")
    screenshot(page, "sessions_launch_ubuntu_form")

    page.locator("#tabSessions button:has-text('Launch')").click()
    page.wait_for_timeout(700)
    screenshot(page, "sessions_ubuntu_session_launched")

    # ------------------------------------------------------------------
    # Step 11 – Launch a Windows 11 session (via API)
    # ------------------------------------------------------------------
    win_sess = api("POST", "/sessions/launch", {
        "user_id": "alice",
        "os_profile": "windows-11",
        "cpu_cores": 2,
        "ram_gb": 4,
    }, token=token)
    win_session_id = win_sess.get("session_id", "")

    # Refresh session list in the UI
    page.locator("#tabSessions button:has-text('Refresh')").click()
    page.wait_for_timeout(700)
    screenshot(page, "sessions_windows11_session_launched")

    # Capture the session IDs from the UI table for later
    page.wait_for_selector("#sessTable", state="visible")
    screenshot(page, "sessions_active_list")

    # ------------------------------------------------------------------
    # Step 12 – Get first session id from the list via API
    # ------------------------------------------------------------------
    sessions_resp = api("GET", "/sessions", token=token)
    sessions = sessions_resp.get("sessions", [])
    first_session_id = sessions[0]["session_id"] if sessions else ""
    print(f"       first session id: {first_session_id}")

    # Visit the session detail JSON
    page.goto(f"{BASE_URL}/sessions/{first_session_id}",
              wait_until="networkidle")
    screenshot(page, "session_detail_json")
    page.goto(f"{BASE_URL}/dashboard")
    page.wait_for_selector("#appShell", state="visible", timeout=8_000)
    page.wait_for_timeout(400)

    # ------------------------------------------------------------------
    # Step 13 – Create a developer workspace (via UI)
    # ------------------------------------------------------------------
    page.click("text=🗂️ Workspaces")
    page.wait_for_selector("#tabWorkspaces", state="visible")
    page.fill("#wsUser", "alice")
    page.fill("#wsName", "my-dev-env")
    page.select_option("#wsOS", "ubuntu-22.04")
    page.fill("#wsCPU", "2")
    page.fill("#wsRAM", "4")
    screenshot(page, "workspaces_create_form")

    page.locator("#tabWorkspaces button:has-text('Create')").click()
    page.wait_for_timeout(700)
    screenshot(page, "workspaces_created")

    # Refresh workspace list
    page.locator("#tabWorkspaces button:has-text('Refresh')").click()
    page.wait_for_timeout(700)
    screenshot(page, "workspaces_list")

    # ------------------------------------------------------------------
    # Step 14 – Snapshot the workspace (via API)
    # ------------------------------------------------------------------
    ws_resp = api("GET", "/workspaces", token=token)
    workspaces = ws_resp.get("workspaces", [])
    workspace_id = workspaces[0]["workspace_id"] if workspaces else ""
    print(f"       workspace id: {workspace_id}")

    snap_resp = api("POST", "/workspaces/snapshot", {
        "workspace_id": workspace_id,
        "snapshot_name": "snap-v1",
    }, token=token)
    print(f"       snapshot: {snap_resp}")

    # Show snapshot result in the browser as JSON
    page.goto(f"{BASE_URL}/workspaces/{workspace_id}", wait_until="networkidle")
    screenshot(page, "workspace_detail_after_snapshot")

    # ------------------------------------------------------------------
    # Step 15 – Clone the workspace (via API)
    # ------------------------------------------------------------------
    clone_resp = api("POST", "/workspaces/clone", {
        "source_workspace_id": workspace_id,
        "new_name": "my-dev-env-clone",
        "new_user_id": "alice",
    }, token=token)
    clone_id = clone_resp.get("workspace_id", "")
    print(f"       clone id: {clone_id}")

    page.goto(f"{BASE_URL}/workspaces/{clone_id}", wait_until="networkidle")
    screenshot(page, "workspace_clone_detail")

    # Back to dashboard workspaces tab
    page.goto(f"{BASE_URL}/dashboard")
    page.wait_for_selector("#appShell", state="visible", timeout=8_000)
    page.click("text=🗂️ Workspaces")
    page.wait_for_selector("#tabWorkspaces", state="visible")
    page.locator("#tabWorkspaces button:has-text('Refresh')").click()
    page.wait_for_timeout(700)
    screenshot(page, "workspaces_list_after_clone")

    # ------------------------------------------------------------------
    # Step 16 – Cluster health check (JSON via browser)
    # ------------------------------------------------------------------
    page.goto(
        f"{BASE_URL}/cluster/health",
        wait_until="networkidle",
        referer=f"{BASE_URL}/dashboard",
    )
    # Inject token via Authorization header is impossible from plain browser GET,
    # so we hit the endpoint via the API and display the result on the page.
    health = api("GET", "/cluster/health", token=token)
    page.goto(f"{BASE_URL}/dashboard")
    page.wait_for_selector("#appShell", state="visible", timeout=8_000)
    page.click("text=🖧 Cluster")
    page.wait_for_selector("#tabCluster", state="visible")
    page.locator("#tabCluster button:has-text('Refresh')").click()
    page.wait_for_timeout(700)
    screenshot(page, "cluster_health_nodes_view")

    # ------------------------------------------------------------------
    # Step 17 – Resource usage via Dev Tools API Explorer
    # ------------------------------------------------------------------
    page.click("text=🛠️ Dev Tools")
    page.wait_for_selector("#tabDeveloper", state="visible")
    page.select_option("#apiMethod", "GET")
    page.fill("#apiPath", "/cluster/resources")
    screenshot(page, "devtools_resource_usage_ready")
    page.locator("#tabDeveloper button:has-text('Send')").click()
    page.wait_for_timeout(800)
    screenshot(page, "devtools_resource_usage_result")

    # ------------------------------------------------------------------
    # Step 18 – /status via Dev Tools
    # ------------------------------------------------------------------
    page.fill("#apiPath", "/status")
    page.locator("#tabDeveloper button:has-text('Send')").click()
    page.wait_for_timeout(700)
    screenshot(page, "devtools_status_result")

    # ------------------------------------------------------------------
    # Step 19 – Terminate the first OS session (via UI)
    # ------------------------------------------------------------------
    page.click("text=🚀 Sessions")
    page.wait_for_selector("#tabSessions", state="visible")
    page.locator("#tabSessions button:has-text('Refresh')").click()
    page.wait_for_timeout(700)
    screenshot(page, "sessions_before_terminate")

    # Terminate via API and refresh
    if first_session_id:
        api("DELETE", f"/sessions/{first_session_id}", token=token)
    page.locator("#tabSessions button:has-text('Refresh')").click()
    page.wait_for_timeout(700)
    screenshot(page, "sessions_after_terminate")

    # ------------------------------------------------------------------
    # Step 20 – Swagger UI
    # ------------------------------------------------------------------
    page.goto(f"{BASE_URL}/docs", wait_until="networkidle")
    page.wait_for_timeout(3000)
    screenshot(page, "swagger_ui_docs")

    # ------------------------------------------------------------------
    # Step 21 – ReDoc UI
    # ------------------------------------------------------------------
    page.goto(f"{BASE_URL}/redoc", wait_until="networkidle")
    page.wait_for_timeout(3000)
    screenshot(page, "redoc_ui_docs")

    # ------------------------------------------------------------------
    # Step 22 – Final dashboard overview (post journey)
    # ------------------------------------------------------------------
    page.goto(f"{BASE_URL}/dashboard")
    page.wait_for_selector("#appShell", state="visible", timeout=8_000)
    page.click("text=📊 Overview")
    page.wait_for_timeout(800)
    screenshot(page, "dashboard_final_overview")

    print(f"\n  ✅  All screenshots saved to: {_SCREENSHOTS}\n")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    server_proc = start_server()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-dev-shm-usage"],
            )
            ctx = browser.new_context(
                viewport={"width": 1440, "height": 900},
                color_scheme="dark",
            )
            page = ctx.new_page()

            print("=" * 60)
            print("  WekezaOmniOS Cloud Desktop — End-to-End Journey")
            print(f"  Screenshots → {_SCREENSHOTS}")
            print("=" * 60)

            run_journey(page)

            ctx.close()
            browser.close()
    finally:
        stop_server(server_proc)


if __name__ == "__main__":
    main()

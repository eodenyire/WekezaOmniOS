#!/usr/bin/env python3
"""
WekezaOmniOS Interface Emulation — End-to-End Integration Test
===============================================================
Standalone script (no pytest) that demonstrates the full
interface-emulation subsystem in action.

Steps:
    1. Create an InterfaceEmulation instance with initial_skin="windows"
    2. Core kernel layer: mount filesystems, spawn processes, add NIC
    3. Command translation: translate a batch of Windows commands
    4. Load Windows UI and render desktop
    5. Switch from Windows to Ubuntu UI
    6. Load a Windows binary through the compat layer
    7. Switch to macOS UI
    8. Print final status summary
    9. Report pass/fail for each step
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from interface_emulation import InterfaceEmulation

print("\n" + "=" * 70)
print("  🔥 WekezaOmniOS Interface Emulation — Integration Test Suite")
print("=" * 70)

results: list[dict] = []


def test_step(name: str, passed: bool, details: str = "") -> None:
    """Records and prints a test step result."""
    status = "✅ PASS" if passed else "❌ FAIL"
    results.append({"name": name, "passed": passed, "details": details})
    print(f"    {status} — {name}")
    if details:
        print(f"           {details}")


# ──────────────────────────────────────────────────────────────────────────
# Step 1: Create InterfaceEmulation instance
# ──────────────────────────────────────────────────────────────────────────
print("\n" + "─" * 70)
print("📦 Step 1: Initialise InterfaceEmulation (initial_skin=windows)")
print("─" * 70)

ie = None
try:
    ie = InterfaceEmulation(host_os="linux", initial_skin="windows")
    test_step(
        "Create InterfaceEmulation",
        ie is not None,
        f"host_os={ie.host_os}, skin={ie.desktop.current_environment}",
    )
except Exception as exc:
    test_step("Create InterfaceEmulation", False, str(exc))
    print("\n❌ Fatal: Cannot continue without InterfaceEmulation. Exiting.")
    sys.exit(1)

# ──────────────────────────────────────────────────────────────────────────
# Step 2: Core kernel layer
# ──────────────────────────────────────────────────────────────────────────
print("\n" + "─" * 70)
print("📦 Step 2: Core Kernel Layer — filesystem, processes, network")
print("─" * 70)

try:
    ie.filesystem.mount("/dev/sda1", "/", "ext4")
    ie.filesystem.mount("/dev/sda2", "/home", "ext4")
    ie.filesystem.mount("tmpfs", "/tmp", "tmpfs")
    mounts = ie.filesystem.list_mounts()
    test_step("Mount filesystems", len(mounts) == 3, f"{len(mounts)} mounts")
except Exception as exc:
    test_step("Mount filesystems", False, str(exc))

try:
    pid1 = ie.launch_app("explorer.exe", os_type="windows")
    pid2 = ie.launch_app("bash",          os_type="linux")
    pid3 = ie.launch_app("com.bank.app",  os_type="android")
    procs = ie.process_mgr.list_processes()
    test_step(
        "Spawn processes",
        len(procs) >= 3,
        f"PIDs: {pid1}, {pid2}, {pid3}",
    )
except Exception as exc:
    test_step("Spawn processes", False, str(exc))

try:
    ie.network.add_interface("eth0", "192.168.1.10")
    ie.network.add_interface("lo",   "127.0.0.1", "255.0.0.0")
    ifaces = ie.network.list_interfaces()
    test_step(
        "Add network interfaces",
        len(ifaces) >= 2,
        f"{len(ifaces)} interface(s)",
    )
except Exception as exc:
    test_step("Add network interfaces", False, str(exc))

try:
    reachable = ie.network.ping("8.8.8.8")
    dns_result = ie.network.resolve("omnios.dev")
    test_step(
        "Ping and DNS resolve",
        reachable and dns_result.startswith("10."),
        f"ping=True, dns={dns_result}",
    )
except Exception as exc:
    test_step("Ping and DNS resolve", False, str(exc))

# ──────────────────────────────────────────────────────────────────────────
# Step 3: Command translation
# ──────────────────────────────────────────────────────────────────────────
print("\n" + "─" * 70)
print("📦 Step 3: Command Translation — Windows → Linux batch")
print("─" * 70)

try:
    from command_translator import CommandTranslator
    ct = CommandTranslator(source_os="windows")
    batch = ct.translate_batch(
        ["dir", "copy", "move", "del", "tasklist", "ipconfig", "shutdown"]
    )
    expected = {
        "dir": "ls", "copy": "cp", "move": "mv",
        "del": "rm", "tasklist": "ps aux",
        "ipconfig": "ifconfig", "shutdown": "shutdown",
    }
    all_ok = all(r["translated"] == expected[r["source"]] for r in batch)
    test_step(
        "Batch command translation",
        all_ok,
        f"{len(batch)} commands translated",
    )
except Exception as exc:
    test_step("Batch command translation", False, str(exc))

# ──────────────────────────────────────────────────────────────────────────
# Step 4: Load Windows UI and render desktop
# ──────────────────────────────────────────────────────────────────────────
print("\n" + "─" * 70)
print("📦 Step 4: Windows UI — render desktop")
print("─" * 70)

try:
    win_skin = ie.desktop.load_skin("windows")
    desktop_output = win_skin.render_desktop()
    test_step(
        "Windows desktop render",
        len(desktop_output) > 0 and "Windows" in desktop_output,
        f"Output length: {len(desktop_output)} chars",
    )
except Exception as exc:
    test_step("Windows desktop render", False, str(exc))

# ──────────────────────────────────────────────────────────────────────────
# Step 5: Switch Windows → Ubuntu
# ──────────────────────────────────────────────────────────────────────────
print("\n" + "─" * 70)
print("📦 Step 5: Switch environment — Windows → Ubuntu")
print("─" * 70)

try:
    ie.switch_ui("ubuntu")
    test_step(
        "Switch to Ubuntu UI",
        ie.desktop.current_environment == "ubuntu",
        f"Active env: {ie.desktop.current_environment}",
    )
    ubuntu_output = ie.desktop.load_skin("ubuntu").render_desktop()
    test_step(
        "Ubuntu desktop render",
        len(ubuntu_output) > 0 and "Ubuntu" in ubuntu_output,
        f"Output length: {len(ubuntu_output)} chars",
    )
except Exception as exc:
    test_step("Switch to Ubuntu UI", False, str(exc))

# ──────────────────────────────────────────────────────────────────────────
# Step 6: Load a Windows binary through the compat layer
# ──────────────────────────────────────────────────────────────────────────
print("\n" + "─" * 70)
print("📦 Step 6: Windows binary loading via compat layer")
print("─" * 70)

try:
    info = ie.load_binary("C:\\Program Files\\OmniApp\\omniapp.exe",
                          os_type="windows")
    test_step(
        "Load Windows .exe",
        info.get("format") == "PE32+" and "loaded" in info.get("status", ""),
        f"format={info.get('format')}, status={info.get('status')}",
    )
except Exception as exc:
    test_step("Load Windows .exe", False, str(exc))

try:
    info = ie.load_binary("/opt/apps/com.omnios.app.apk", os_type="android")
    test_step(
        "Load Android .apk",
        "APK" in info.get("format", ""),
        f"format={info.get('format')}",
    )
except Exception as exc:
    test_step("Load Android .apk", False, str(exc))

# ──────────────────────────────────────────────────────────────────────────
# Step 7: Switch to macOS UI
# ──────────────────────────────────────────────────────────────────────────
print("\n" + "─" * 70)
print("📦 Step 7: Switch environment — Ubuntu → macOS")
print("─" * 70)

try:
    ie.switch_ui("macos")
    test_step(
        "Switch to macOS UI",
        ie.desktop.current_environment == "macos",
        f"Active env: {ie.desktop.current_environment}",
    )
    macos_output = ie.desktop.load_skin("macos").render_desktop()
    test_step(
        "macOS desktop render",
        len(macos_output) > 0 and "macOS" in macos_output,
        f"Output length: {len(macos_output)} chars",
    )
except Exception as exc:
    test_step("Switch to macOS UI", False, str(exc))

# ──────────────────────────────────────────────────────────────────────────
# Step 8: Final status summary
# ──────────────────────────────────────────────────────────────────────────
print("\n" + "─" * 70)
print("📦 Step 8: Full status summary")
print("─" * 70)

try:
    ie.status()
    test_step("Status summary", True, "Printed without error")
except Exception as exc:
    test_step("Status summary", False, str(exc))

# ──────────────────────────────────────────────────────────────────────────
# Step 9: Final report
# ──────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("  📊 Integration Test Results")
print("=" * 70)

passed = [r for r in results if r["passed"]]
failed = [r for r in results if not r["passed"]]

for r in results:
    status = "✅" if r["passed"] else "❌"
    print(f"  {status}  {r['name']}")

print()
print(f"  Total : {len(results)}")
print(f"  Passed: {len(passed)}")
print(f"  Failed: {len(failed)}")

if failed:
    print("\n  Failed steps:")
    for r in failed:
        print(f"    ❌ {r['name']}: {r['details']}")
    print("\n❌ Integration test completed WITH FAILURES.")
    sys.exit(1)
else:
    print("\n✅ All integration tests PASSED.")
    sys.exit(0)

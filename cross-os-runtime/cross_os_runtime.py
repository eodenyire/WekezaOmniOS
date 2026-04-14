"""
WekezaOmniOS Cross-OS Runtime — Top-level Orchestrator
=======================================================
Wires together all six sub-systems of the Cross-OS Runtime Layer into a
single runtime object that the CLI, SDK, and monitoring layers interact
with.

End-to-end flow:
    1. An application is installed via the AppManager.
    2. The AppManager consults the SyscallTranslator for the right
       compatibility module.
    3. The RuntimeEngine schedules and allocates resources for the process.
    4. The Sandbox isolates the process using namespaces + seccomp.
    5. The UICompositor surfaces the application window on the desktop.
"""

import os
import sys

# Resolve sibling package paths when the file is run directly
_BASE = os.path.dirname(os.path.abspath(__file__))
for _sub in (
    os.path.join(_BASE, "runtime-core"),
    os.path.join(_BASE, "app-manager"),
    os.path.join(_BASE, "sandbox"),
    os.path.join(_BASE, "system-call-translator"),
    os.path.join(_BASE, "ui-integration"),
    os.path.join(_BASE, "compatibility-modules"),
):
    if _sub not in sys.path:
        sys.path.insert(0, _sub)

from runtime_engine import RuntimeEngine
from app_manager import AppManager
from sandbox import Sandbox
from syscall_translator import SyscallTranslator
from ui_compositor import UICompositor
from windows_runtime.windows_runtime import WindowsRuntime
from linux_runtime.linux_runtime import LinuxRuntime
from android_runtime.android_runtime import AndroidRuntime
from legacy_mobile_runtime.legacy_mobile_runtime import LegacyMobileRuntime


# ---------------------------------------------------------------------------
# Compatibility module registry
# ---------------------------------------------------------------------------

_COMPAT_MODULES = {
    "windows":       WindowsRuntime,
    "linux":         LinuxRuntime,
    "android":       AndroidRuntime,
    "legacy_mobile": LegacyMobileRuntime,
}


class CrossOSRuntime:
    """
    High-level façade for the Cross-OS Runtime Layer.

    Instantiate once and use ``install``, ``launch``, ``suspend``,
    ``resume``, and ``kill`` to manage cross-OS applications.
    """

    def __init__(self, host_os="linux",
                 desktop_width=1920, desktop_height=1080):
        """
        Args:
            host_os (str): Underlying OS the runtime is hosted on.
            desktop_width (int): Virtual desktop width in pixels.
            desktop_height (int): Virtual desktop height in pixels.
        """
        print("\n" + "=" * 60)
        print("  WekezaOmniOS Cross-OS Runtime — Starting Up")
        print("=" * 60)

        self.sandbox    = Sandbox()
        self.engine     = RuntimeEngine(host_os=host_os)
        self.app_mgr    = AppManager(sandbox=self.sandbox)
        self.compositor = UICompositor(desktop_width, desktop_height)

        # Per-OS syscall translators (lazy-initialised)
        self._translators = {}

        print("\n[CrossOSRuntime] ✅ All sub-systems online.\n")

    # ------------------------------------------------------------------
    # Application management
    # ------------------------------------------------------------------

    def install(self, app_id, name, os_type, entry_point, metadata=None):
        """
        Registers an application with the runtime.

        Args:
            app_id (str): Unique application identifier.
            name (str): Human-readable name.
            os_type (str): Source OS.
            entry_point (str): Main binary or class.
            metadata (dict | None): Optional extra fields.

        Returns:
            AppRecord: The installed application record.
        """
        return self.app_mgr.install_app(
            app_id, name, os_type, entry_point, metadata
        )

    def launch(self, app_id, priority=5, memory_mb=64,
               win_x=0, win_y=0, win_w=800, win_h=600):
        """
        Launches an installed application end-to-end:
          1. Translate any incoming OS snapshot through the compat module.
          2. Launch via AppManager (assigns PID, optionally sandboxes).
          3. Register with the RuntimeEngine for scheduling.
          4. Surface a window via the UICompositor.

        Args:
            app_id (str): Application to launch.
            priority (int): Scheduler priority (1–10).
            memory_mb (int): Initial heap in MiB.
            win_x, win_y (int): Initial window position.
            win_w, win_h (int): Initial window dimensions.

        Returns:
            AppRecord | None: Updated record, or None on failure.
        """
        record = self.app_mgr.launch_app(
            app_id, priority=priority, memory_mb=memory_mb
        )
        if not record:
            return None

        # Register process with the runtime engine
        self.engine.launch(
            pid=record.pid,
            name=record.name,
            os_type=record.os_type,
            priority=priority,
            memory_bytes=memory_mb * 1024 * 1024,
        )

        # Register window with compositor
        win_id = f"win:{app_id}"
        self.compositor.register_window(
            win_id=win_id,
            app_id=app_id,
            title=record.name,
            os_type=record.os_type,
            x=win_x, y=win_y,
            width=win_w, height=win_h,
        )

        return record

    def suspend(self, app_id):
        """Suspends a running application."""
        self.app_mgr.suspend_app(app_id)
        record = self.app_mgr.get_app(app_id)
        if record and record.pid:
            self.engine.suspend(record.pid)
        self.compositor.set_state(f"win:{app_id}", "minimised")

    def resume(self, app_id):
        """Resumes a suspended application."""
        self.app_mgr.resume_app(app_id)
        record = self.app_mgr.get_app(app_id)
        if record and record.pid:
            self.engine.resume(record.pid)
        self.compositor.set_state(f"win:{app_id}", "normal")

    def kill(self, app_id):
        """Terminates an application and reclaims all resources."""
        record = self.app_mgr.get_app(app_id)
        if record and record.pid:
            self.engine.terminate(record.pid)
            self.sandbox.release(record.pid)
        self.app_mgr.kill_app(app_id)
        self.compositor.close_window(f"win:{app_id}")

    # ------------------------------------------------------------------
    # Translation helpers
    # ------------------------------------------------------------------

    def translate_syscall(self, os_type, syscall_name):
        """
        Translates a single syscall from *os_type* to the Linux equivalent.

        Args:
            os_type (str): Source OS.
            syscall_name (str): Syscall to translate.

        Returns:
            str: Linux equivalent syscall name.
        """
        if os_type not in self._translators:
            self._translators[os_type] = SyscallTranslator(source_os=os_type)
        return self._translators[os_type].translate(syscall_name)

    def get_compat_module(self, os_type):
        """
        Returns an instantiated compatibility module for *os_type*.

        Args:
            os_type (str): Source OS name.

        Returns:
            WindowsRuntime | LinuxRuntime | AndroidRuntime |
            LegacyMobileRuntime | None
        """
        cls = _COMPAT_MODULES.get(os_type.lower())
        if cls is None:
            print(f"[CrossOSRuntime] ⚠️  No compat module for {os_type!r}.")
            return None
        return cls()

    # ------------------------------------------------------------------
    # Status
    # ------------------------------------------------------------------

    def status(self):
        """
        Returns a combined status report from all sub-systems.

        Returns:
            dict: Runtime status snapshot.
        """
        import json
        engine_status = self.engine.status()
        scene = self.compositor.render_scene()
        apps = [a.to_dict() for a in self.app_mgr.list_apps()]
        report = {
            "engine":     engine_status,
            "apps":       apps,
            "compositor": scene,
        }
        return report


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import json

    runtime = CrossOSRuntime(host_os="linux")

    # Install applications from three different OS ecosystems
    runtime.install("notepad",      "Notepad Classic",    "windows",
                    "notepad.exe")
    runtime.install("com.bank.app", "Mobile Banking",     "android",
                    "com.bank.MainActivity")
    runtime.install("htop",         "htop",               "linux",
                    "/usr/bin/htop")
    runtime.install("snake_game",   "Snake Game (J2ME)",  "legacy_mobile",
                    "com.midlet.SnakeGame")

    # Launch all applications
    runtime.launch("notepad",       priority=4, memory_mb=32,
                   win_x=100,  win_y=50,  win_w=640, win_h=480)
    runtime.launch("com.bank.app",  priority=6, memory_mb=48,
                   win_x=760,  win_y=50,  win_w=360, win_h=640)
    runtime.launch("htop",          priority=8, memory_mb=16,
                   win_x=100,  win_y=550, win_w=900, win_h=400)
    runtime.launch("snake_game",    priority=3, memory_mb=8,
                   win_x=1100, win_y=150, win_w=240, win_h=320)

    # Simulate scheduling ticks
    runtime.engine.run_ticks(count=4)

    # Show syscall translation
    print("\n--- Syscall translation demo ---")
    runtime.translate_syscall("windows", "NtCreateFile")
    runtime.translate_syscall("android", "BINDER_WRITE_READ")

    # Lifecycle operations
    runtime.suspend("htop")
    runtime.resume("htop")
    runtime.kill("snake_game")

    # Print full status
    report = runtime.status()
    print("\n[CrossOSRuntime] Status Report:")
    print(json.dumps(report, indent=2))

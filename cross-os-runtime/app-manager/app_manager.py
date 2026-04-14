"""
WekezaOmniOS Application Manager
Controls the full lifecycle of applications running inside the
Cross-OS Runtime Layer.

Lifecycle stages:
    install → configure → launch → (suspend | resume) → kill
"""

import os
import json
import time
import threading


class AppRecord:
    """Stores metadata for a managed application."""

    def __init__(self, app_id, name, os_type, entry_point, install_dir):
        self.app_id      = app_id
        self.name        = name
        self.os_type     = os_type          # windows | linux | android | legacy_mobile
        self.entry_point = entry_point      # main binary / class / activity
        self.install_dir = install_dir
        self.state       = "installed"      # installed | running | suspended | killed
        self.pid         = None
        self.started_at  = None

    def to_dict(self):
        return {
            "app_id":      self.app_id,
            "name":        self.name,
            "os_type":     self.os_type,
            "entry_point": self.entry_point,
            "install_dir": self.install_dir,
            "state":       self.state,
            "pid":         self.pid,
            "started_at":  self.started_at,
        }

    def __repr__(self):
        return (
            f"<AppRecord id={self.app_id!r} name={self.name!r} "
            f"os={self.os_type} state={self.state}>"
        )


class AppManager:
    """
    Manages installation and lifecycle of cross-OS applications.

    Responsibilities:
    - Register (install) applications and persist their metadata.
    - Launch, suspend, resume, and kill processes.
    - Delegate sandboxing decisions to the Sandbox component.
    - Provide a full application registry for the UI and CLI layers.
    """

    def __init__(self, app_root="/tmp/omni_apps", sandbox=None):
        """
        Args:
            app_root (str): Root directory under which app data is stored.
            sandbox: Optional Sandbox instance; if provided, each launched
                     app is placed in an isolated container automatically.
        """
        self._lock    = threading.Lock()
        self._apps    = {}          # app_id -> AppRecord
        self._pid_seq = 9000        # synthetic PID counter for demo
        self.app_root = app_root
        self.sandbox  = sandbox
        os.makedirs(app_root, exist_ok=True)
        print(f"[AppManager] Initialised. App root: {app_root}")

    # ------------------------------------------------------------------
    # Installation
    # ------------------------------------------------------------------

    def install_app(self, app_id, name, os_type, entry_point,
                    metadata=None):
        """
        Registers an application with the runtime.

        Args:
            app_id (str): Unique application identifier.
            name (str): Human-readable application name.
            os_type (str): Source OS.
            entry_point (str): Binary / class / activity to launch.
            metadata (dict | None): Optional extra metadata to persist.

        Returns:
            AppRecord: The newly created application record.
        """
        with self._lock:
            if app_id in self._apps:
                print(f"[AppManager] ⚠️  '{app_id}' already installed.")
                return self._apps[app_id]

            install_dir = os.path.join(self.app_root, app_id)
            os.makedirs(install_dir, exist_ok=True)

            record = AppRecord(app_id, name, os_type, entry_point,
                               install_dir)
            self._apps[app_id] = record

            # Persist metadata
            meta = {"record": record.to_dict()}
            if metadata:
                meta.update(metadata)
            self._write_meta(install_dir, meta)

            print(f"[AppManager] ✅ Installed: {record}")
            return record

    # ------------------------------------------------------------------
    # Launch
    # ------------------------------------------------------------------

    def launch_app(self, app_id, priority=5, memory_mb=64):
        """
        Launches an installed application inside the runtime.

        Args:
            app_id (str): Application to launch.
            priority (int): Scheduler priority (1–10).
            memory_mb (int): Initial heap allocation in MiB.

        Returns:
            AppRecord | None: Updated record, or None on failure.
        """
        with self._lock:
            record = self._apps.get(app_id)
            if not record:
                print(f"[AppManager] ❌ Unknown app: {app_id!r}")
                return None
            if record.state == "running":
                print(f"[AppManager] ⚠️  '{app_id}' is already running.")
                return record

            # Assign a synthetic PID
            self._pid_seq += 1
            record.pid        = self._pid_seq
            record.state      = "running"
            record.started_at = time.strftime("%Y-%m-%dT%H:%M:%S")

            print(
                f"[AppManager] 🚀 Launching '{record.name}' "
                f"(app_id={app_id}, pid={record.pid}, "
                f"os={record.os_type}, priority={priority}, "
                f"memory={memory_mb}MiB)"
            )

            # Optionally place in sandbox
            if self.sandbox:
                self.sandbox_app(app_id)

            return record

    # ------------------------------------------------------------------
    # Suspend / Resume
    # ------------------------------------------------------------------

    def suspend_app(self, app_id):
        """Suspends a running application."""
        with self._lock:
            record = self._get_running(app_id)
            if record:
                record.state = "suspended"
                print(
                    f"[AppManager] ⏸  '{record.name}' "
                    f"(PID {record.pid}) suspended."
                )

    def resume_app(self, app_id):
        """Resumes a suspended application."""
        with self._lock:
            record = self._apps.get(app_id)
            if record and record.state == "suspended":
                record.state = "running"
                print(
                    f"[AppManager] ▶️  '{record.name}' "
                    f"(PID {record.pid}) resumed."
                )

    # ------------------------------------------------------------------
    # Kill
    # ------------------------------------------------------------------

    def kill_app(self, app_id):
        """
        Terminates a running or suspended application.

        Args:
            app_id (str): Application to terminate.
        """
        with self._lock:
            record = self._apps.get(app_id)
            if not record:
                print(f"[AppManager] ❌ Unknown app: {app_id!r}")
                return
            if record.state == "killed":
                print(f"[AppManager] ⚠️  '{app_id}' is already killed.")
                return

            print(
                f"[AppManager] 🛑 Killing '{record.name}' "
                f"(PID {record.pid})..."
            )
            record.state = "killed"
            record.pid   = None
            print(f"[AppManager] '{record.name}' terminated.")

    # ------------------------------------------------------------------
    # Sandbox delegation
    # ------------------------------------------------------------------

    def sandbox_app(self, app_id):
        """
        Places an application into a security sandbox.

        Args:
            app_id (str): Application to isolate.
        """
        record = self._apps.get(app_id)
        if not record:
            print(f"[AppManager] ❌ Cannot sandbox unknown app: {app_id!r}")
            return

        if self.sandbox:
            self.sandbox.isolate(record.pid, record.name)
        else:
            print(
                f"[AppManager] ℹ️  No sandbox configured — "
                f"'{record.name}' running unsandboxed."
            )

    # ------------------------------------------------------------------
    # Registry
    # ------------------------------------------------------------------

    def list_apps(self, state_filter=None):
        """
        Returns all registered application records.

        Args:
            state_filter (str | None): If given, only apps in this state
                                       are returned.

        Returns:
            list[AppRecord]: Matching application records.
        """
        with self._lock:
            apps = list(self._apps.values())
        if state_filter:
            apps = [a for a in apps if a.state == state_filter]
        return apps

    def get_app(self, app_id):
        """Returns the AppRecord for *app_id* or None."""
        return self._apps.get(app_id)

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _get_running(self, app_id):
        record = self._apps.get(app_id)
        if not record:
            print(f"[AppManager] ❌ Unknown app: {app_id!r}")
            return None
        if record.state != "running":
            print(
                f"[AppManager] ⚠️  '{app_id}' is not running "
                f"(state={record.state})."
            )
            return None
        return record

    @staticmethod
    def _write_meta(directory, data):
        path = os.path.join(directory, "metadata.json")
        with open(path, "w") as f:
            json.dump(data, f, indent=4)


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    manager = AppManager()

    manager.install_app(
        "notepad",
        name="Notepad Classic",
        os_type="windows",
        entry_point="notepad.exe",
        metadata={"version": "5.1"},
    )
    manager.install_app(
        "com.bank.app",
        name="Mobile Banking",
        os_type="android",
        entry_point="com.bank.MainActivity",
    )
    manager.install_app(
        "htop",
        name="htop",
        os_type="linux",
        entry_point="/usr/bin/htop",
    )

    manager.launch_app("notepad",      priority=4, memory_mb=32)
    manager.launch_app("com.bank.app", priority=6, memory_mb=48)
    manager.launch_app("htop",         priority=8, memory_mb=16)

    manager.suspend_app("com.bank.app")
    manager.resume_app("com.bank.app")
    manager.kill_app("htop")

    print("\n[AppManager] All apps:")
    for app in manager.list_apps():
        print(" ", app)

    print("\n[AppManager] Running apps:")
    for app in manager.list_apps(state_filter="running"):
        print(" ", app)

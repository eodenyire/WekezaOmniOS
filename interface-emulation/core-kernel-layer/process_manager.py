"""
WekezaOmniOS Interface Emulation — Process Manager
====================================================
Tracks simulated processes with auto-incrementing PIDs and supports
full lifecycle management: spawn, suspend, resume, and terminate.
"""


class ProcessManager:
    """
    In-memory process table for the interface-emulation kernel layer.

    Processes are identified by auto-incremented integer PIDs.
    """

    def __init__(self):
        print("[ProcessManager] 🔧 Initialising process manager...")
        self._processes: dict[int, dict] = {}
        self._next_pid: int = 1000
        print("[ProcessManager] ✅ Process manager ready.")

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def spawn(self, name: str, os_type: str = "linux", priority: int = 5) -> int:
        """
        Creates a new simulated process.

        Args:
            name (str): Human-readable process name.
            os_type (str): Source OS the process originates from.
            priority (int): Scheduler priority (1–10).

        Returns:
            int: The PID assigned to the new process.
        """
        pid = self._next_pid
        self._next_pid += 1
        self._processes[pid] = {
            "pid": pid,
            "name": name,
            "os_type": os_type,
            "priority": priority,
            "state": "running",
        }
        print(
            f"[ProcessManager] Spawned '{name}' (PID={pid}, os={os_type}, "
            f"priority={priority})"
        )
        return pid

    def terminate(self, pid: int) -> None:
        """
        Terminates and removes a process.

        Args:
            pid (int): Process to terminate.

        Raises:
            ValueError: If *pid* is not tracked.
        """
        if pid not in self._processes:
            raise ValueError(f"[ProcessManager] PID {pid} not found.")
        name = self._processes[pid]["name"]
        del self._processes[pid]
        print(f"[ProcessManager] Terminated '{name}' (PID={pid})")

    def suspend(self, pid: int) -> None:
        """
        Changes a process state to 'suspended'.

        Args:
            pid (int): Target PID.

        Raises:
            ValueError: If *pid* is not tracked.
        """
        if pid not in self._processes:
            raise ValueError(f"[ProcessManager] PID {pid} not found.")
        self._processes[pid]["state"] = "suspended"
        name = self._processes[pid]["name"]
        print(f"[ProcessManager] Suspended '{name}' (PID={pid})")

    def resume(self, pid: int) -> None:
        """
        Resumes a suspended process.

        Args:
            pid (int): Target PID.

        Raises:
            ValueError: If *pid* is not tracked.
        """
        if pid not in self._processes:
            raise ValueError(f"[ProcessManager] PID {pid} not found.")
        self._processes[pid]["state"] = "running"
        name = self._processes[pid]["name"]
        print(f"[ProcessManager] Resumed '{name}' (PID={pid})")

    # ------------------------------------------------------------------
    # Introspection
    # ------------------------------------------------------------------

    def list_processes(self) -> list[dict]:
        """Returns a list of all tracked process dicts."""
        return list(self._processes.values())

    def get_process(self, pid: int) -> dict | None:
        """
        Returns the process dict for *pid*, or None if not found.

        Args:
            pid (int): Target PID.

        Returns:
            dict | None
        """
        return self._processes.get(pid)


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    pm = ProcessManager()
    pid1 = pm.spawn("bash", "linux", priority=7)
    pid2 = pm.spawn("notepad.exe", "windows", priority=4)
    pm.suspend(pid2)
    pm.resume(pid2)
    pm.terminate(pid1)
    print(pm.list_processes())

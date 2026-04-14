"""
WekezaOmniOS Runtime Engine
Main orchestrator for the Cross-OS Runtime Layer.

The RuntimeEngine ties together the ProcessScheduler, MemoryManager,
and ResourceAbstractor into a single entry point that the rest of the
system interacts with.
"""

import time
import os
import sys

# Allow sibling imports when run as a script
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from scheduler import ProcessScheduler
from memory_manager import MemoryManager
from resource_abstractor import ResourceAbstractor


class RuntimeEngine:
    """
    Central execution engine for the Cross-OS Runtime Layer.

    Responsibilities:
    - Accept application launch requests from the AppManager.
    - Coordinate scheduling, memory allocation, and resource quotas.
    - Provide a status dashboard for the monitoring subsystem.
    """

    def __init__(self, host_os="linux", max_memory_per_process=None):
        """
        Args:
            host_os (str): The underlying OS the runtime is hosted on.
            max_memory_per_process (int | None): Per-process RAM ceiling
                in bytes; uses MemoryManager default when None.
        """
        print("[RuntimeEngine] 🚀 Initialising Cross-OS Runtime Layer...")
        self.host_os = host_os
        self.scheduler = ProcessScheduler()
        self.memory = MemoryManager(max_per_process_bytes=max_memory_per_process)
        self.resources = ResourceAbstractor(host_os=host_os)
        self._running = False
        print("[RuntimeEngine] ✅ Runtime engine ready.")

    # ------------------------------------------------------------------
    # Process lifecycle
    # ------------------------------------------------------------------

    def launch(self, pid, name, os_type, priority=5,
               memory_bytes=64 * 1024 * 1024):
        """
        Launches an application process inside the runtime.

        Args:
            pid (int): Process identifier assigned by the AppManager.
            name (str): Application name.
            os_type (str): Source OS ('windows', 'linux', 'android', etc.).
            priority (int): Scheduler priority (1–10).
            memory_bytes (int): Initial heap allocation in bytes.

        Returns:
            bool: True when the process was successfully admitted.
        """
        print(f"[RuntimeEngine] Launching '{name}' (PID={pid}, os={os_type})")

        # 1. Verify resource headroom
        if not self.resources.check_quota(pid, "memory", memory_bytes):
            print(f"[RuntimeEngine] ❌ Insufficient memory quota for PID {pid}.")
            return False

        # 2. Allocate initial heap region
        region = self.memory.allocate(pid, memory_bytes, label="heap")
        if region is None:
            print(f"[RuntimeEngine] ❌ Memory allocation failed for PID {pid}.")
            return False

        # 3. Register with the scheduler
        self.scheduler.register(pid, name, os_type, priority=priority)

        # 4. Record initial resource usage
        self.resources.record_usage(pid, "memory", memory_bytes)

        print(f"[RuntimeEngine] ✅ '{name}' (PID={pid}) is live.")
        return True

    def suspend(self, pid):
        """Suspends a running process."""
        self.scheduler.suspend(pid)

    def resume(self, pid):
        """Resumes a suspended process."""
        self.scheduler.resume(pid)

    def terminate(self, pid):
        """
        Terminates a process and reclaims all its resources.

        Args:
            pid (int): Target process identifier.
        """
        print(f"[RuntimeEngine] 🛑 Terminating PID {pid}...")
        self.scheduler.terminate(pid)
        self.memory.free_all(pid)
        self.resources.release_resources(pid)
        print(f"[RuntimeEngine] PID {pid} fully removed from runtime.")

    # ------------------------------------------------------------------
    # Scheduling loop
    # ------------------------------------------------------------------

    def tick(self):
        """
        Advances the scheduler by one time quantum.

        Returns:
            ProcessEntry | None: The process given CPU time this tick.
        """
        return self.scheduler.next_process()

    def run_ticks(self, count=1):
        """
        Runs *count* scheduling ticks, simulating CPU time slices.

        Args:
            count (int): Number of ticks to execute.
        """
        print(f"\n[RuntimeEngine] ⏱  Running {count} scheduling tick(s)...")
        for i in range(count):
            proc = self.tick()
            if proc:
                time.sleep(0)   # yield; replace with actual work in production
        print(f"[RuntimeEngine] Tick run complete.\n")

    # ------------------------------------------------------------------
    # Introspection
    # ------------------------------------------------------------------

    def status(self):
        """
        Returns a status report for the runtime engine.

        Returns:
            dict: Snapshot of active processes and memory usage.
        """
        procs = [
            {
                "pid": p.pid,
                "name": p.name,
                "os": p.os_type,
                "state": p.state,
                "priority": p.priority,
            }
            for p in self.scheduler.list_processes()
        ]
        return {
            "host_os": self.host_os,
            "active_processes": procs,
            "memory_usage_bytes": self.memory.snapshot(),
        }


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    engine = RuntimeEngine(host_os="linux")

    engine.launch(3001, "notepad.exe",   "windows", priority=4,
                  memory_bytes=32 * 1024 * 1024)
    engine.launch(3002, "bash",          "linux",   priority=8,
                  memory_bytes=16 * 1024 * 1024)
    engine.launch(3003, "com.bank.app",  "android", priority=6,
                  memory_bytes=48 * 1024 * 1024)

    engine.run_ticks(count=6)

    engine.suspend(3002)
    engine.resume(3002)
    engine.terminate(3003)

    import json
    print("[RuntimeEngine] Status report:")
    print(json.dumps(engine.status(), indent=2))

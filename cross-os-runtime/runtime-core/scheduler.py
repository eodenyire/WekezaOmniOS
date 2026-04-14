"""
WekezaOmniOS Process Scheduler
Manages scheduling of processes across the universal runtime layer.
Supports round-robin and priority-based scheduling strategies.
"""

import time
from collections import deque


class ProcessEntry:
    """Represents a tracked process inside the runtime scheduler."""

    def __init__(self, pid, name, os_type, priority=5):
        self.pid = pid
        self.name = name
        self.os_type = os_type
        self.priority = priority          # 1 (lowest) to 10 (highest)
        self.state = "ready"              # ready | running | suspended | terminated
        self.created_at = time.time()
        self.cpu_time = 0.0               # accumulated CPU time in seconds

    def __repr__(self):
        return (
            f"<ProcessEntry pid={self.pid} name={self.name!r} "
            f"os={self.os_type} priority={self.priority} state={self.state}>"
        )


class ProcessScheduler:
    """
    Universal process scheduler for the Cross-OS Runtime Layer.

    Tracks processes from multiple OS environments and arbitrates CPU
    access using a round-robin queue with optional priority boosting.
    """

    def __init__(self):
        self._processes = {}          # pid -> ProcessEntry
        self._ready_queue = deque()   # ordered list of ready pids

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register(self, pid, name, os_type, priority=5):
        """
        Registers a new process with the scheduler.

        Args:
            pid (int): Process identifier.
            name (str): Human-readable application name.
            os_type (str): Source OS (e.g. 'windows', 'linux', 'android').
            priority (int): Scheduling priority between 1 and 10.

        Returns:
            ProcessEntry: The newly created entry.
        """
        if pid in self._processes:
            print(f"[Scheduler] ⚠️  PID {pid} already registered — skipping.")
            return self._processes[pid]

        entry = ProcessEntry(pid, name, os_type, priority)
        self._processes[pid] = entry
        self._ready_queue.append(pid)
        print(f"[Scheduler] ✅ Registered {entry}")
        return entry

    # ------------------------------------------------------------------
    # State transitions
    # ------------------------------------------------------------------

    def suspend(self, pid):
        """Moves a running process to the suspended state."""
        entry = self._get(pid)
        if entry:
            entry.state = "suspended"
            print(f"[Scheduler] ⏸  PID {pid} ({entry.name}) suspended.")

    def resume(self, pid):
        """Resumes a suspended process and re-queues it."""
        entry = self._get(pid)
        if entry and entry.state == "suspended":
            entry.state = "ready"
            self._ready_queue.append(pid)
            print(f"[Scheduler] ▶️  PID {pid} ({entry.name}) resumed.")

    def terminate(self, pid):
        """Marks a process as terminated and removes it from the queue."""
        entry = self._get(pid)
        if entry:
            entry.state = "terminated"
            self._processes.pop(pid, None)
            print(f"[Scheduler] 🛑 PID {pid} ({entry.name}) terminated.")

    # ------------------------------------------------------------------
    # Scheduling tick
    # ------------------------------------------------------------------

    def next_process(self):
        """
        Returns the next process to be given CPU time (round-robin).

        Higher-priority processes are cycled to the front when there is
        more than one candidate in the queue.

        Returns:
            ProcessEntry | None: The next process or None if queue is empty.
        """
        if not self._ready_queue:
            return None

        # Soft priority boost: pick highest-priority among first N entries
        sample_size = min(len(self._ready_queue), 4)
        candidates = [self._ready_queue[i] for i in range(sample_size)]
        best_pid = max(
            candidates,
            key=lambda p: self._processes[p].priority if p in self._processes else 0,
        )

        # Rotate queue so best_pid moves to end (standard round-robin after boost)
        self._ready_queue.remove(best_pid)
        self._ready_queue.append(best_pid)

        entry = self._processes.get(best_pid)
        if entry:
            entry.state = "running"
            print(
                f"[Scheduler] 🔄 Dispatching PID {best_pid} ({entry.name}, "
                f"os={entry.os_type}, priority={entry.priority})"
            )
        return entry

    # ------------------------------------------------------------------
    # Introspection
    # ------------------------------------------------------------------

    def list_processes(self):
        """Returns a list of all currently tracked process entries."""
        return list(self._processes.values())

    def _get(self, pid):
        entry = self._processes.get(pid)
        if not entry:
            print(f"[Scheduler] ❌ PID {pid} not found.")
        return entry


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    scheduler = ProcessScheduler()

    scheduler.register(1001, "notepad.exe", "windows", priority=3)
    scheduler.register(1002, "bash",         "linux",   priority=7)
    scheduler.register(1003, "calculator",   "android", priority=5)

    for _ in range(5):
        proc = scheduler.next_process()
        if proc:
            print(f"  → Running: {proc.name}\n")

    scheduler.suspend(1002)
    scheduler.resume(1002)
    scheduler.terminate(1003)
    print("\n[Scheduler] Active processes:", scheduler.list_processes())

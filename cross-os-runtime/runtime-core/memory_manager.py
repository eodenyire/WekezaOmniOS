"""
WekezaOmniOS Memory Manager
Tracks and enforces per-process memory allocations within the
universal runtime layer.
"""

import threading


class MemoryRegion:
    """Represents an allocated memory block owned by a process."""

    def __init__(self, region_id, pid, size_bytes, label="heap"):
        self.region_id = region_id
        self.pid = pid
        self.size_bytes = size_bytes
        self.label = label          # heap | stack | mmap | shared

    def __repr__(self):
        return (
            f"<MemoryRegion id={self.region_id} pid={self.pid} "
            f"size={self.size_bytes}B label={self.label!r}>"
        )


class MemoryManager:
    """
    Manages virtual memory allocations for all processes running inside
    the Cross-OS Runtime Layer.

    Responsibilities:
    - Allocate and release memory regions per process.
    - Enforce a configurable per-process memory ceiling.
    - Provide memory usage snapshots for the runtime engine.
    """

    DEFAULT_MAX_BYTES = 512 * 1024 * 1024   # 512 MiB per process

    def __init__(self, max_per_process_bytes=None):
        self._lock = threading.Lock()
        self._regions = {}              # region_id -> MemoryRegion
        self._pid_regions = {}          # pid -> list[region_id]
        self._next_id = 1
        self._max = max_per_process_bytes or self.DEFAULT_MAX_BYTES

    # ------------------------------------------------------------------
    # Allocation
    # ------------------------------------------------------------------

    def allocate(self, pid, size_bytes, label="heap"):
        """
        Allocates a memory region for a process.

        Args:
            pid (int): Owning process identifier.
            size_bytes (int): Number of bytes to allocate.
            label (str): Region type tag (heap, stack, mmap, shared).

        Returns:
            MemoryRegion | None: The allocated region, or None on failure.
        """
        with self._lock:
            current = self._usage(pid)
            if current + size_bytes > self._max:
                print(
                    f"[MemoryManager] ❌ PID {pid}: allocation of {size_bytes}B "
                    f"would exceed limit ({self._max}B). Current usage: {current}B."
                )
                return None

            region_id = self._next_id
            self._next_id += 1
            region = MemoryRegion(region_id, pid, size_bytes, label)
            self._regions[region_id] = region
            self._pid_regions.setdefault(pid, []).append(region_id)
            print(
                f"[MemoryManager] ✅ Allocated {size_bytes}B for PID {pid} "
                f"(region={region_id}, label={label!r})."
            )
            return region

    def free(self, region_id):
        """
        Frees a previously allocated memory region.

        Args:
            region_id (int): The region identifier returned by allocate().
        """
        with self._lock:
            region = self._regions.pop(region_id, None)
            if region is None:
                print(f"[MemoryManager] ⚠️  Region {region_id} not found.")
                return
            self._pid_regions.get(region.pid, []).remove(region_id)
            print(
                f"[MemoryManager] 🗑  Freed region {region_id} "
                f"({region.size_bytes}B) for PID {region.pid}."
            )

    def free_all(self, pid):
        """
        Releases all memory regions owned by a process.

        Args:
            pid (int): Process whose regions should be freed.
        """
        with self._lock:
            ids = list(self._pid_regions.pop(pid, []))
            for region_id in ids:
                self._regions.pop(region_id, None)
            print(f"[MemoryManager] 🗑  Freed all {len(ids)} region(s) for PID {pid}.")

    # ------------------------------------------------------------------
    # Introspection
    # ------------------------------------------------------------------

    def usage(self, pid):
        """Returns the total bytes currently allocated to *pid*."""
        with self._lock:
            return self._usage(pid)

    def snapshot(self):
        """
        Returns a usage snapshot for all active processes.

        Returns:
            dict: Mapping of pid -> bytes_used.
        """
        with self._lock:
            result = {}
            for pid, ids in self._pid_regions.items():
                result[pid] = sum(
                    self._regions[rid].size_bytes
                    for rid in ids
                    if rid in self._regions
                )
            return result

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _usage(self, pid):
        """Returns bytes used by *pid* (caller must hold _lock)."""
        ids = self._pid_regions.get(pid, [])
        return sum(
            self._regions[rid].size_bytes
            for rid in ids
            if rid in self._regions
        )


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    mm = MemoryManager(max_per_process_bytes=1024)

    r1 = mm.allocate(1001, 256, label="heap")
    r2 = mm.allocate(1001, 512, label="stack")
    r3 = mm.allocate(1001, 512, label="heap")   # should fail (exceeds 1024)

    print(f"\nUsage for PID 1001: {mm.usage(1001)}B")
    print(f"Snapshot: {mm.snapshot()}")

    mm.free(r1.region_id)
    mm.free_all(1001)
    print(f"Snapshot after free: {mm.snapshot()}")

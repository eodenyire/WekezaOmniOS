"""
Resource Allocator — tracks and enforces CPU / RAM quota for sessions
running inside the Cloud Desktop cluster.
"""

import threading
from typing import Optional


class ResourceAllocator:
    """Tracks per-session resource allocation and enforces cluster-level quotas."""

    # Default per-session limits
    DEFAULT_CPU_CORES = 2
    DEFAULT_RAM_GB = 4

    def __init__(self, total_cpu_cores: int = 32, total_ram_gb: int = 128):
        self.total_cpu = total_cpu_cores
        self.total_ram = total_ram_gb
        self._allocations: dict[str, dict] = {}
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Allocation lifecycle
    # ------------------------------------------------------------------

    def allocate(self, session_id: str, cpu_cores: int = DEFAULT_CPU_CORES,
                 ram_gb: int = DEFAULT_RAM_GB) -> dict:
        with self._lock:
            used_cpu = sum(a["cpu_cores"] for a in self._allocations.values())
            used_ram = sum(a["ram_gb"] for a in self._allocations.values())

            if used_cpu + cpu_cores > self.total_cpu:
                raise RuntimeError(
                    f"Insufficient CPU: requested {cpu_cores}, available {self.total_cpu - used_cpu}"
                )
            if used_ram + ram_gb > self.total_ram:
                raise RuntimeError(
                    f"Insufficient RAM: requested {ram_gb} GB, available {self.total_ram - used_ram} GB"
                )

            record = {"session_id": session_id, "cpu_cores": cpu_cores, "ram_gb": ram_gb}
            self._allocations[session_id] = record
            return record

    def release(self, session_id: str) -> bool:
        with self._lock:
            if session_id not in self._allocations:
                return False
            del self._allocations[session_id]
            return True

    # ------------------------------------------------------------------
    # Inspection
    # ------------------------------------------------------------------

    def usage(self) -> dict:
        with self._lock:
            used_cpu = sum(a["cpu_cores"] for a in self._allocations.values())
            used_ram = sum(a["ram_gb"] for a in self._allocations.values())
            return {
                "total_cpu_cores": self.total_cpu,
                "used_cpu_cores": used_cpu,
                "free_cpu_cores": self.total_cpu - used_cpu,
                "total_ram_gb": self.total_ram,
                "used_ram_gb": used_ram,
                "free_ram_gb": self.total_ram - used_ram,
                "active_sessions": len(self._allocations),
            }

    def get_allocation(self, session_id: str) -> Optional[dict]:
        with self._lock:
            return self._allocations.get(session_id)

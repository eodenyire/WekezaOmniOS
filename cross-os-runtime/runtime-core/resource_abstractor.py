"""
WekezaOmniOS Resource Abstractor
Presents a unified hardware and OS resource interface to the runtime engine,
hiding differences between underlying host platforms.
"""


# Canonical resource identifiers used across the runtime
RESOURCE_TYPES = ("cpu", "memory", "disk", "network", "gpu")


class ResourceAbstractor:
    """
    Abstracts host hardware resources for processes running inside the
    Cross-OS Runtime Layer.

    Responsibilities:
    - Publish a normalised view of available host resources.
    - Map OS-specific resource APIs to the universal interface.
    - Enforce resource quotas and mediate access between processes.
    """

    def __init__(self, host_os="linux"):
        """
        Args:
            host_os (str): The underlying OS the runtime is hosted on
                           ('linux', 'windows', 'macos').
        """
        self.host_os = host_os.lower()
        self._quotas = {}       # pid -> dict of resource -> limit
        self._usage = {}        # pid -> dict of resource -> current usage
        print(f"[ResourceAbstractor] Initialised for host OS: {self.host_os}")

    # ------------------------------------------------------------------
    # Resource discovery
    # ------------------------------------------------------------------

    def available_resources(self):
        """
        Returns a dictionary describing abstractly available resources on
        the host.  Values are illustrative ceiling estimates; a real
        implementation would query psutil / WMI / sysfs.

        Returns:
            dict: resource name -> available capacity (arbitrary units).
        """
        resources = {
            "cpu":     self._query_cpu(),
            "memory":  self._query_memory(),
            "disk":    self._query_disk(),
            "network": self._query_network(),
            "gpu":     self._query_gpu(),
        }
        print(f"[ResourceAbstractor] Available resources: {resources}")
        return resources

    # ------------------------------------------------------------------
    # Quota management
    # ------------------------------------------------------------------

    def set_quota(self, pid, resource, limit):
        """
        Assigns a resource ceiling for a specific process.

        Args:
            pid (int): Target process identifier.
            resource (str): One of RESOURCE_TYPES.
            limit: Maximum allowed value (units depend on resource type).
        """
        if resource not in RESOURCE_TYPES:
            print(f"[ResourceAbstractor] ⚠️  Unknown resource type: {resource!r}")
            return
        self._quotas.setdefault(pid, {})[resource] = limit
        print(
            f"[ResourceAbstractor] Quota set — PID {pid}: "
            f"{resource}={limit}"
        )

    def check_quota(self, pid, resource, requested):
        """
        Checks whether a resource request is within the process quota.

        Args:
            pid (int): Process identifier.
            resource (str): Resource type to check.
            requested: The requested amount.

        Returns:
            bool: True if within quota (or no quota set), False otherwise.
        """
        limit = self._quotas.get(pid, {}).get(resource)
        if limit is None:
            return True
        current = self._usage.get(pid, {}).get(resource, 0)
        allowed = (current + requested) <= limit
        if not allowed:
            print(
                f"[ResourceAbstractor] ❌ Quota exceeded — PID {pid}: "
                f"{resource} request={requested}, used={current}, limit={limit}"
            )
        return allowed

    def record_usage(self, pid, resource, amount):
        """
        Records observed resource consumption for a process.

        Args:
            pid (int): Process identifier.
            resource (str): Resource type.
            amount: Usage delta to accumulate.
        """
        self._usage.setdefault(pid, {})[resource] = (
            self._usage.get(pid, {}).get(resource, 0) + amount
        )

    def release_resources(self, pid):
        """
        Clears all usage records and quotas for a terminated process.

        Args:
            pid (int): Process identifier.
        """
        self._quotas.pop(pid, None)
        self._usage.pop(pid, None)
        print(f"[ResourceAbstractor] Released all resources for PID {pid}.")

    # ------------------------------------------------------------------
    # Host-specific query helpers
    # ------------------------------------------------------------------

    def _query_cpu(self):
        """Returns logical CPU count (or a safe default)."""
        try:
            import os
            return os.cpu_count() or 1
        except Exception:
            return 1

    def _query_memory(self):
        """Returns available RAM in bytes (or a safe default)."""
        try:
            import psutil
            return psutil.virtual_memory().available
        except Exception:
            return 4 * 1024 * 1024 * 1024   # 4 GiB fallback

    def _query_disk(self):
        """Returns free disk space in bytes for the root path."""
        try:
            import shutil
            return shutil.disk_usage("/").free
        except Exception:
            return 50 * 1024 * 1024 * 1024  # 50 GiB fallback

    def _query_network(self):
        """Returns a nominal network bandwidth estimate in Mbps."""
        return 1000   # 1 Gbps nominal

    def _query_gpu(self):
        """Returns available GPU memory in bytes, or 0 if no GPU detected."""
        try:
            import subprocess
            out = subprocess.check_output(
                ["nvidia-smi", "--query-gpu=memory.free", "--format=csv,noheader,nounits"],
                stderr=subprocess.DEVNULL,
                text=True,
            )
            return int(out.strip().split("\n")[0]) * 1024 * 1024
        except Exception:
            return 0


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    abstractor = ResourceAbstractor(host_os="linux")

    abstractor.available_resources()

    abstractor.set_quota(2001, "cpu", 2)
    abstractor.set_quota(2001, "memory", 256 * 1024 * 1024)

    print(abstractor.check_quota(2001, "cpu", 1))       # True
    print(abstractor.check_quota(2001, "cpu", 3))       # False

    abstractor.record_usage(2001, "cpu", 1)
    abstractor.release_resources(2001)

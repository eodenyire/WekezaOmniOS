"""
Control Plane — top-level orchestrator that wires together the NodePool,
ResourceAllocator, ClusterScheduler, and NodeMonitor.

Import this module to get a ready-to-use ControlPlane singleton.
"""

import os
import sys

# Allow sibling package imports when run standalone
_CLOUD_MODEL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _CLOUD_MODEL_DIR not in sys.path:
    sys.path.insert(0, _CLOUD_MODEL_DIR)

from compute_nodes.node_pool import NodePool          # noqa: E402
from control_plane.resource_allocator import ResourceAllocator  # noqa: E402
from control_plane.cluster_scheduler import ClusterScheduler    # noqa: E402
from control_plane.node_monitor import NodeMonitor              # noqa: E402


class ControlPlane:
    """
    Central orchestrator for the Cloud Desktop cluster.

    Usage::

        cp = ControlPlane()
        cp.start_monitor()
        session = cp.launch_session(user_id="alice", os_profile="ubuntu-22.04")
        cp.terminate_session(session["session_id"])
    """

    def __init__(self,
                 registry_path: str = None,
                 total_cpu_cores: int = 32,
                 total_ram_gb: int = 128,
                 monitor_interval: int = 30):

        if registry_path is None:
            registry_path = os.path.join(
                _CLOUD_MODEL_DIR, "compute-nodes", "node_pool_registry.json"
            )

        self.node_pool = NodePool(registry_path=registry_path)
        self.allocator = ResourceAllocator(
            total_cpu_cores=total_cpu_cores,
            total_ram_gb=total_ram_gb,
        )
        self.scheduler = ClusterScheduler(self.node_pool, self.allocator)
        self.monitor = NodeMonitor(self.node_pool, poll_interval_seconds=monitor_interval)

    # ------------------------------------------------------------------
    # Monitor lifecycle
    # ------------------------------------------------------------------

    def start_monitor(self) -> None:
        self.monitor.start()

    def stop_monitor(self) -> None:
        self.monitor.stop()

    # ------------------------------------------------------------------
    # Session management
    # ------------------------------------------------------------------

    def launch_session(self, user_id: str, os_profile: str,
                       cpu_cores: int = 2, ram_gb: int = 4) -> dict:
        return self.scheduler.schedule(
            user_id=user_id,
            os_profile=os_profile,
            cpu_cores=cpu_cores,
            ram_gb=ram_gb,
        )

    def terminate_session(self, session_id: str) -> dict:
        return self.scheduler.terminate(session_id)

    # ------------------------------------------------------------------
    # Node management
    # ------------------------------------------------------------------

    def add_node(self, node_id: str, node_type: str, address: str,
                 cpu_cores: int = 4, ram_gb: int = 8) -> dict:
        return self.node_pool.add_node(
            node_id=node_id,
            node_type=node_type,
            address=address,
            cpu_cores=cpu_cores,
            ram_gb=ram_gb,
        )

    def remove_node(self, node_id: str) -> bool:
        return self.node_pool.remove_node(node_id)

    def list_nodes(self, node_type: str = None, status: str = None) -> list:
        return self.node_pool.list_nodes(node_type=node_type, status=status)

    # ------------------------------------------------------------------
    # Observability
    # ------------------------------------------------------------------

    def resource_usage(self) -> dict:
        return self.allocator.usage()

    def node_health(self, node_id: str) -> dict:
        return self.monitor.health(node_id)

    def cluster_health(self) -> list:
        return self.monitor.health_all()

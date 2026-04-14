"""
Cluster Scheduler — decides which compute node should host a new session
based on node type, availability, and current load.
"""

import uuid
from typing import Optional


class ClusterScheduler:
    """
    Schedules incoming session requests to appropriate compute nodes.
    Strategy: prefer idle nodes; fall back to least-loaded active node.
    """

    OS_TO_NODE_TYPE = {
        "ubuntu-22.04": "linux",
        "debian-12": "linux",
        "fedora-39": "linux",
        "arch-latest": "linux",
        "windows-11": "windows",
        "windows-10": "windows",
        "windows-server-2022": "windows",
        "android-14": "android-emulator",
        "android-13": "android-emulator",
        "android-12": "android-emulator",
        "android-11": "android-emulator",
    }

    def __init__(self, node_pool, resource_allocator):
        self.node_pool = node_pool
        self.allocator = resource_allocator

    def schedule(self, user_id: str, os_profile: str,
                 cpu_cores: int = 2, ram_gb: int = 4) -> dict:
        """
        Allocate resources, pick a node, and start a session.

        Returns a session record dict on success, raises RuntimeError on failure.
        """
        node_type = self.OS_TO_NODE_TYPE.get(os_profile)
        if node_type is None:
            # Default to Linux for unknown profiles
            node_type = "linux"

        node = self.node_pool.pick_available(node_type)
        if node is None:
            raise RuntimeError(
                f"No compute node available for node_type={node_type!r}. "
                "Register nodes via the API first."
            )

        session_id = f"sess-{uuid.uuid4().hex[:12]}"

        # Reserve resources
        self.allocator.allocate(session_id, cpu_cores=cpu_cores, ram_gb=ram_gb)

        try:
            session = node.start_session(
                session_id=session_id,
                user_id=user_id,
                os_profile=os_profile,
            )
        except Exception:
            self.allocator.release(session_id)
            raise

        session["allocated_cpu"] = cpu_cores
        session["allocated_ram_gb"] = ram_gb
        return session

    def terminate(self, session_id: str) -> dict:
        """Stop a session and free its resources."""
        result = None
        for node in self.node_pool.nodes.values():
            if session_id in node.sessions:
                result = node.stop_session(session_id)
                break

        self.allocator.release(session_id)

        if result is None:
            return {"status": "not_found", "session_id": session_id}
        return result

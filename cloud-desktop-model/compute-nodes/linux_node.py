"""
Linux compute node for the Cloud Desktop Model.
Simulates a containerised Linux desktop session delivered over WebSocket/VNC.
"""

import datetime
import uuid

from .node_base import NodeBase


class LinuxNode(NodeBase):
    """Compute node that hosts Linux desktop sessions."""

    NODE_TYPE = "linux"

    SUPPORTED_PROFILES = ("ubuntu-22.04", "debian-12", "fedora-39", "arch-latest")

    def start_session(self, session_id: str, user_id: str, os_profile: str = "ubuntu-22.04") -> dict:
        if os_profile not in self.SUPPORTED_PROFILES:
            os_profile = "ubuntu-22.04"

        session = self._make_session(
            session_id=session_id,
            user_id=user_id,
            os_profile=os_profile,
            extra={
                "display_protocol": "vnc",
                "vnc_port": 5900 + (len(self.sessions) % 100),
                "display": f":{len(self.sessions) + 1}",
                "container_id": f"ctr-{session_id[:8]}",
            },
        )
        self.sessions[session_id] = session
        self.status = "active"
        return session

    def stop_session(self, session_id: str) -> dict:
        session = self.sessions.pop(session_id, None)
        if session is None:
            return {"status": "not_found", "session_id": session_id}

        if not self.sessions:
            self.status = "idle"

        return {
            "status": "stopped",
            "session_id": session_id,
            "node_id": self.node_id,
            "stopped_at": datetime.datetime.utcnow().isoformat() + "Z",
        }

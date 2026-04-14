"""
Windows compute node for the Cloud Desktop Model.
Simulates a Windows desktop session delivered over RDP.
"""

import datetime

from .node_base import NodeBase


class WindowsNode(NodeBase):
    """Compute node that hosts Windows desktop sessions."""

    NODE_TYPE = "windows"

    SUPPORTED_PROFILES = ("windows-11", "windows-10", "windows-server-2022")

    def start_session(self, session_id: str, user_id: str, os_profile: str = "windows-11") -> dict:
        if os_profile not in self.SUPPORTED_PROFILES:
            os_profile = "windows-11"

        session = self._make_session(
            session_id=session_id,
            user_id=user_id,
            os_profile=os_profile,
            extra={
                "display_protocol": "rdp",
                "rdp_port": 3389 + (len(self.sessions) % 100),
                "vm_id": f"vm-{session_id[:8]}",
                "connect_url": f"rdp://{self.address}:{3389 + (len(self.sessions) % 100)}",
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

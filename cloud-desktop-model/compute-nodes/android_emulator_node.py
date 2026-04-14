"""
Android emulator compute node for the Cloud Desktop Model.
Simulates an Android emulator session delivered over a web-based ADB bridge.
"""

import datetime

from .node_base import NodeBase


class AndroidEmulatorNode(NodeBase):
    """Compute node that hosts Android emulator sessions."""

    NODE_TYPE = "android-emulator"

    SUPPORTED_PROFILES = ("android-14", "android-13", "android-12", "android-11")

    def start_session(self, session_id: str, user_id: str, os_profile: str = "android-14") -> dict:
        if os_profile not in self.SUPPORTED_PROFILES:
            os_profile = "android-14"

        api_level_map = {
            "android-14": 34,
            "android-13": 33,
            "android-12": 32,
            "android-11": 30,
        }

        session = self._make_session(
            session_id=session_id,
            user_id=user_id,
            os_profile=os_profile,
            extra={
                "display_protocol": "webrtc",
                "api_level": api_level_map.get(os_profile, 34),
                "avd_name": f"avd-{session_id[:8]}",
                "adb_port": 5554 + (len(self.sessions) % 100),
                "connect_url": f"https://{self.address}/emulator/{session_id}",
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

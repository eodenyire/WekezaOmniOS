"""
OS Launcher Controller — delegates session launch/terminate to the
ControlPlane and tracks active sessions.
"""

import os
import sys

_CLOUD_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _CLOUD_DIR not in sys.path:
    sys.path.insert(0, _CLOUD_DIR)

from control_plane.control_plane import ControlPlane  # noqa: E402


class OSLauncherController:
    """Thin façade that delegates to the ControlPlane for OS session management."""

    def __init__(self, control_plane: ControlPlane):
        self.cp = control_plane
        self._sessions: dict[str, dict] = {}

    def launch(self, user_id: str, os_profile: str,
               cpu_cores: int = 2, ram_gb: int = 4) -> dict:
        session = self.cp.launch_session(
            user_id=user_id,
            os_profile=os_profile,
            cpu_cores=cpu_cores,
            ram_gb=ram_gb,
        )
        self._sessions[session["session_id"]] = session
        return session

    def terminate(self, session_id: str) -> dict:
        result = self.cp.terminate_session(session_id)
        self._sessions.pop(session_id, None)
        return result

    def list_sessions(self, user_id: str = None) -> list:
        sessions = list(self._sessions.values())
        if user_id:
            sessions = [s for s in sessions if s.get("user_id") == user_id]
        return sessions

    def get_session(self, session_id: str) -> dict:
        return self._sessions.get(session_id)

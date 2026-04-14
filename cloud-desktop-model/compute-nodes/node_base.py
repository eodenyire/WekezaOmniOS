"""
Base class for all compute nodes in the Cloud Desktop Model.
Each node type (Linux, Windows, Android) extends this interface.
"""

import datetime
from abc import ABC, abstractmethod
from typing import Optional


class NodeBase(ABC):
    """Abstract base class for a cloud desktop compute node."""

    NODE_TYPE: str = "base"

    def __init__(self, node_id: str, address: str, cpu_cores: int = 4, ram_gb: int = 8):
        self.node_id = node_id
        self.address = address
        self.cpu_cores = cpu_cores
        self.ram_gb = ram_gb
        self.status = "idle"
        self.sessions: dict = {}
        self.created_at = datetime.datetime.utcnow().isoformat() + "Z"

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    @abstractmethod
    def start_session(self, session_id: str, user_id: str, os_profile: str) -> dict:
        """Allocate and start a new desktop session on this node."""

    @abstractmethod
    def stop_session(self, session_id: str) -> dict:
        """Terminate an existing session and free its resources."""

    # ------------------------------------------------------------------
    # Shared helpers
    # ------------------------------------------------------------------

    def get_session(self, session_id: str) -> Optional[dict]:
        return self.sessions.get(session_id)

    def list_sessions(self) -> list:
        return list(self.sessions.values())

    def health(self) -> dict:
        return {
            "node_id": self.node_id,
            "node_type": self.NODE_TYPE,
            "address": self.address,
            "status": self.status,
            "active_sessions": len(self.sessions),
            "cpu_cores": self.cpu_cores,
            "ram_gb": self.ram_gb,
        }

    def to_dict(self) -> dict:
        return {
            "node_id": self.node_id,
            "node_type": self.NODE_TYPE,
            "address": self.address,
            "status": self.status,
            "cpu_cores": self.cpu_cores,
            "ram_gb": self.ram_gb,
            "active_sessions": len(self.sessions),
            "created_at": self.created_at,
        }

    def _make_session(self, session_id: str, user_id: str, os_profile: str, extra: Optional[dict] = None) -> dict:
        record = {
            "session_id": session_id,
            "user_id": user_id,
            "os_profile": os_profile,
            "node_id": self.node_id,
            "node_type": self.NODE_TYPE,
            "status": "running",
            "started_at": datetime.datetime.utcnow().isoformat() + "Z",
            "connect_url": f"wss://{self.address}/session/{session_id}",
        }
        if extra:
            record.update(extra)
        return record

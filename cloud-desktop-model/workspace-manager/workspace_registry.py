"""
Workspace Registry — persists workspace records as JSON so they survive
server restarts.
"""

import json
import os
import threading
from typing import Optional


class WorkspaceRegistry:
    """Thread-safe JSON-backed registry for workspace records."""

    def __init__(self, registry_path: Optional[str] = None):
        self.registry_path = registry_path or os.path.join(
            os.path.dirname(__file__), "workspace_registry.json"
        )
        self._lock = threading.Lock()
        self._data: dict[str, dict] = {}
        self._load()

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def _load(self) -> None:
        if not os.path.exists(self.registry_path):
            return
        try:
            with open(self.registry_path, "r", encoding="utf-8") as f:
                self._data = json.load(f)
        except (json.JSONDecodeError, IOError):
            self._data = {}

    def _save(self) -> None:
        os.makedirs(os.path.dirname(os.path.abspath(self.registry_path)), exist_ok=True)
        with open(self.registry_path, "w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=2)

    # ------------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------------

    def put(self, workspace_id: str, record: dict) -> None:
        with self._lock:
            self._data[workspace_id] = record
            self._save()

    def get(self, workspace_id: str) -> Optional[dict]:
        with self._lock:
            return self._data.get(workspace_id)

    def delete(self, workspace_id: str) -> bool:
        with self._lock:
            if workspace_id not in self._data:
                return False
            del self._data[workspace_id]
            self._save()
            return True

    def list_all(self, user_id: Optional[str] = None) -> list:
        with self._lock:
            records = list(self._data.values())
        if user_id:
            records = [r for r in records if r.get("user_id") == user_id]
        return records

    def exists(self, workspace_id: str) -> bool:
        with self._lock:
            return workspace_id in self._data

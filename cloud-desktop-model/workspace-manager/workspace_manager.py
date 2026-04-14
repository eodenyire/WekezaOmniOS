"""
Workspace Manager — implements start_workspace(), clone_workspace(), and
snapshot_workspace() for the Cloud Desktop Model.

Each workspace represents a persistent, named developer environment tied to
a user.  Under the hood a workspace is a record in the registry that tracks
the active session, OS profile, and any snapshots.
"""

import datetime
import json
import os
import uuid
from typing import Optional

from .workspace_registry import WorkspaceRegistry


class WorkspaceManager:
    """
    Manages developer workspace lifecycle within the Cloud Desktop Model.

    Usage::

        wm = WorkspaceManager()
        ws = wm.start_workspace(user_id="alice", name="my-env", os_profile="ubuntu-22.04")
        clone = wm.clone_workspace(ws["workspace_id"], new_name="my-env-fork")
        snap = wm.snapshot_workspace(ws["workspace_id"])
        wm.stop_workspace(ws["workspace_id"])
    """

    def __init__(self,
                 registry_path: Optional[str] = None,
                 snapshot_dir: Optional[str] = None,
                 control_plane=None):
        self.registry = WorkspaceRegistry(registry_path=registry_path)

        if snapshot_dir is None:
            snapshot_dir = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "data", "workspace-snapshots",
            )
        self.snapshot_dir = snapshot_dir
        os.makedirs(self.snapshot_dir, exist_ok=True)

        # Optional: wired to the ControlPlane to actually launch sessions
        self.control_plane = control_plane

    # ------------------------------------------------------------------
    # Core operations
    # ------------------------------------------------------------------

    def start_workspace(self, user_id: str, name: str,
                        os_profile: str = "ubuntu-22.04",
                        cpu_cores: int = 2, ram_gb: int = 4) -> dict:
        """Create and start a new workspace, launching an OS session if a
        ControlPlane is available."""

        workspace_id = f"ws-{uuid.uuid4().hex[:10]}"
        session = None

        if self.control_plane is not None:
            session = self.control_plane.launch_session(
                user_id=user_id,
                os_profile=os_profile,
                cpu_cores=cpu_cores,
                ram_gb=ram_gb,
            )

        record = {
            "workspace_id": workspace_id,
            "user_id": user_id,
            "name": name,
            "os_profile": os_profile,
            "status": "running" if session else "created",
            "session": session,
            "snapshots": [],
            "created_at": datetime.datetime.utcnow().isoformat() + "Z",
            "updated_at": datetime.datetime.utcnow().isoformat() + "Z",
        }

        self.registry.put(workspace_id, record)
        return record

    def stop_workspace(self, workspace_id: str) -> dict:
        """Stop an active workspace and its underlying session."""
        record = self.registry.get(workspace_id)
        if record is None:
            return {"status": "not_found", "workspace_id": workspace_id}

        session_id = (record.get("session") or {}).get("session_id")
        if session_id and self.control_plane is not None:
            self.control_plane.terminate_session(session_id)

        record["status"] = "stopped"
        record["session"] = None
        record["updated_at"] = datetime.datetime.utcnow().isoformat() + "Z"
        self.registry.put(workspace_id, record)
        return {"status": "stopped", "workspace_id": workspace_id}

    def get_workspace(self, workspace_id: str) -> Optional[dict]:
        return self.registry.get(workspace_id)

    def list_workspaces(self, user_id: Optional[str] = None) -> list:
        return self.registry.list_all(user_id=user_id)

    def delete_workspace(self, workspace_id: str) -> dict:
        self.stop_workspace(workspace_id)
        deleted = self.registry.delete(workspace_id)
        return {"status": "deleted" if deleted else "not_found", "workspace_id": workspace_id}

    # ------------------------------------------------------------------
    # Clone
    # ------------------------------------------------------------------

    def clone_workspace(self, source_workspace_id: str, new_name: str,
                        new_user_id: Optional[str] = None) -> dict:
        """Fork an existing workspace into a new independent copy."""
        source = self.registry.get(source_workspace_id)
        if source is None:
            raise ValueError(f"Source workspace not found: {source_workspace_id}")

        new_id = f"ws-{uuid.uuid4().hex[:10]}"
        clone = {
            "workspace_id": new_id,
            "user_id": new_user_id or source["user_id"],
            "name": new_name,
            "os_profile": source["os_profile"],
            "status": "created",
            "session": None,
            "snapshots": list(source.get("snapshots", [])),
            "cloned_from": source_workspace_id,
            "created_at": datetime.datetime.utcnow().isoformat() + "Z",
            "updated_at": datetime.datetime.utcnow().isoformat() + "Z",
        }
        self.registry.put(new_id, clone)
        return clone

    # ------------------------------------------------------------------
    # Snapshot
    # ------------------------------------------------------------------

    def snapshot_workspace(self, workspace_id: str,
                           snapshot_name: Optional[str] = None) -> dict:
        """Capture the current state of a workspace as a named snapshot."""
        record = self.registry.get(workspace_id)
        if record is None:
            raise ValueError(f"Workspace not found: {workspace_id}")

        ts = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")
        name = snapshot_name or f"snap-{workspace_id}-{ts}"
        snap_path = os.path.join(self.snapshot_dir, f"{name}.json")

        snapshot_record = {
            "snapshot_name": name,
            "workspace_id": workspace_id,
            "user_id": record["user_id"],
            "os_profile": record["os_profile"],
            "session_at_snapshot": record.get("session"),
            "created_at": datetime.datetime.utcnow().isoformat() + "Z",
        }

        with open(snap_path, "w", encoding="utf-8") as f:
            json.dump(snapshot_record, f, indent=2)

        record.setdefault("snapshots", []).append(name)
        record["updated_at"] = datetime.datetime.utcnow().isoformat() + "Z"
        self.registry.put(workspace_id, record)

        return {"status": "ok", "snapshot_name": name, "path": snap_path}

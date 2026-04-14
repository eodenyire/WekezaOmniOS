"""
Workspace Controller — thin façade over the WorkspaceManager.
"""

import os
import sys
from typing import Optional

_CLOUD_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _CLOUD_DIR not in sys.path:
    sys.path.insert(0, _CLOUD_DIR)

from workspace_manager.workspace_manager import WorkspaceManager  # noqa: E402


class WorkspaceController:
    def __init__(self, workspace_manager: WorkspaceManager):
        self.wm = workspace_manager

    def create(self, user_id: str, name: str, os_profile: str,
               cpu_cores: int = 2, ram_gb: int = 4) -> dict:
        return self.wm.start_workspace(
            user_id=user_id, name=name, os_profile=os_profile,
            cpu_cores=cpu_cores, ram_gb=ram_gb,
        )

    def stop(self, workspace_id: str) -> dict:
        return self.wm.stop_workspace(workspace_id)

    def get(self, workspace_id: str) -> Optional[dict]:
        return self.wm.get_workspace(workspace_id)

    def list_all(self, user_id: Optional[str] = None) -> list:
        return self.wm.list_workspaces(user_id=user_id)

    def delete(self, workspace_id: str) -> dict:
        return self.wm.delete_workspace(workspace_id)

    def clone(self, source_id: str, new_name: str, new_user_id: Optional[str] = None) -> dict:
        return self.wm.clone_workspace(source_id, new_name, new_user_id=new_user_id)

    def snapshot(self, workspace_id: str, snapshot_name: Optional[str] = None) -> dict:
        return self.wm.snapshot_workspace(workspace_id, snapshot_name=snapshot_name)

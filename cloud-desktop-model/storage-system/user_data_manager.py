"""
User Data Manager — high-level façade over ObjectStorage and DistributedFS
that provides per-user namespaced data access for the Cloud Desktop Model.
"""

import json
import os

from .object_storage import ObjectStorage
from .distributed_fs import DistributedFS


class UserDataManager:
    """
    Manages user-scoped data stored in object storage and the distributed
    filesystem.  Each user receives isolated buckets and FS directories.
    """

    def __init__(self, storage_root: str):
        obj_root = os.path.join(storage_root, "objects")
        fs_root = os.path.join(storage_root, "fs")
        self.object_store = ObjectStorage(root_dir=obj_root)
        self.dfs = DistributedFS(root_dir=fs_root)

    # ------------------------------------------------------------------
    # Object storage helpers
    # ------------------------------------------------------------------

    def _user_bucket(self, user_id: str) -> str:
        return f"user-{user_id}"

    def put_file(self, user_id: str, key: str, data: bytes,
                 content_type: str = "application/octet-stream") -> dict:
        bucket = self._user_bucket(user_id)
        return self.object_store.put_object(bucket, key, data, content_type)

    def get_file(self, user_id: str, key: str) -> bytes:
        return self.object_store.get_object(self._user_bucket(user_id), key)

    def delete_file(self, user_id: str, key: str) -> dict:
        return self.object_store.delete_object(self._user_bucket(user_id), key)

    def list_files(self, user_id: str, prefix: str = "") -> list:
        return self.object_store.list_objects(self._user_bucket(user_id), prefix=prefix)

    # ------------------------------------------------------------------
    # Filesystem helpers
    # ------------------------------------------------------------------

    def _user_fs_path(self, user_id: str, relative_path: str = "") -> str:
        base = f"/users/{user_id}"
        if relative_path:
            return base + "/" + relative_path.lstrip("/")
        return base

    def mkdir(self, user_id: str, relative_path: str) -> dict:
        return self.dfs.mkdir(self._user_fs_path(user_id, relative_path))

    def write_fs(self, user_id: str, relative_path: str, data: bytes) -> dict:
        return self.dfs.write(self._user_fs_path(user_id, relative_path), data)

    def read_fs(self, user_id: str, relative_path: str) -> bytes:
        return self.dfs.read(self._user_fs_path(user_id, relative_path))

    def listdir(self, user_id: str, relative_path: str = "") -> list:
        return self.dfs.listdir(self._user_fs_path(user_id, relative_path))

    # ------------------------------------------------------------------
    # Workspace profile helpers
    # ------------------------------------------------------------------

    def save_profile(self, user_id: str, profile: dict) -> dict:
        data = json.dumps(profile, indent=2).encode("utf-8")
        return self.put_file(user_id, "profile.json", data, "application/json")

    def load_profile(self, user_id: str) -> dict:
        try:
            data = self.get_file(user_id, "profile.json")
            return json.loads(data)
        except FileNotFoundError:
            return {}

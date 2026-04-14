"""
Storage Manager — top-level façade for the Cloud Desktop storage system.
Instantiates and exposes the object store, distributed FS, and per-user
data manager through a single interface.
"""

import os

from .object_storage import ObjectStorage
from .distributed_fs import DistributedFS
from .user_data_manager import UserDataManager


class StorageManager:
    """
    Central storage entry-point for the Cloud Desktop Model.

    Usage::

        sm = StorageManager(storage_root="/var/wekeza/storage")
        sm.user_data.put_file("alice", "docs/readme.txt", b"hello")
    """

    def __init__(self, storage_root: str = None):
        if storage_root is None:
            storage_root = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "data", "storage",
            )
        self.storage_root = storage_root
        os.makedirs(storage_root, exist_ok=True)

        self.objects = ObjectStorage(root_dir=os.path.join(storage_root, "objects"))
        self.dfs = DistributedFS(root_dir=os.path.join(storage_root, "fs"))
        self.user_data = UserDataManager(storage_root=storage_root)

    def info(self) -> dict:
        buckets = self.objects.list_buckets()
        return {
            "storage_root": self.storage_root,
            "object_buckets": len(buckets),
            "bucket_names": buckets,
        }

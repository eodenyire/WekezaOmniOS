"""
Distributed Filesystem — a Ceph-inspired local simulation for the Cloud
Desktop storage system.  Provides a POSIX-like interface over a local
directory tree with replication metadata.
"""

import datetime
import json
import os
import shutil
from typing import Optional


class DistributedFS:
    """
    Simulates a distributed filesystem (inspired by CephFS).
    In production, this would interface with a real Ceph/GlusterFS cluster.
    """

    def __init__(self, root_dir: str, replication_factor: int = 3):
        self.root = root_dir
        self.replication_factor = replication_factor
        os.makedirs(self.root, exist_ok=True)

    # ------------------------------------------------------------------
    # Directory operations
    # ------------------------------------------------------------------

    def mkdir(self, path: str) -> dict:
        full = self._full_path(path)
        os.makedirs(full, exist_ok=True)
        return {"status": "ok", "path": path}

    def rmdir(self, path: str, recursive: bool = False) -> dict:
        full = self._full_path(path)
        if not os.path.isdir(full):
            return {"status": "not_found", "path": path}
        if recursive:
            shutil.rmtree(full)
        else:
            os.rmdir(full)
        return {"status": "deleted", "path": path}

    def listdir(self, path: str = "/") -> list:
        full = self._full_path(path)
        if not os.path.isdir(full):
            return []
        entries = []
        for name in sorted(os.listdir(full)):
            entry_path = os.path.join(full, name)
            entries.append({
                "name": name,
                "path": os.path.join(path, name),
                "is_dir": os.path.isdir(entry_path),
                "size": os.path.getsize(entry_path) if os.path.isfile(entry_path) else 0,
            })
        return entries

    # ------------------------------------------------------------------
    # File operations
    # ------------------------------------------------------------------

    def write(self, path: str, data: bytes) -> dict:
        full = self._full_path(path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "wb") as f:
            f.write(data)
        return {
            "status": "ok",
            "path": path,
            "size": len(data),
            "replicas": self.replication_factor,
            "written_at": datetime.datetime.utcnow().isoformat() + "Z",
        }

    def read(self, path: str) -> bytes:
        full = self._full_path(path)
        if not os.path.isfile(full):
            raise FileNotFoundError(f"File not found in distributed FS: {path}")
        with open(full, "rb") as f:
            return f.read()

    def delete(self, path: str) -> dict:
        full = self._full_path(path)
        if not os.path.exists(full):
            return {"status": "not_found", "path": path}
        if os.path.isdir(full):
            shutil.rmtree(full)
        else:
            os.remove(full)
        return {"status": "deleted", "path": path}

    def stat(self, path: str) -> Optional[dict]:
        full = self._full_path(path)
        if not os.path.exists(full):
            return None
        st = os.stat(full)
        return {
            "path": path,
            "size": st.st_size,
            "is_dir": os.path.isdir(full),
            "mtime": datetime.datetime.utcfromtimestamp(st.st_mtime).isoformat() + "Z",
        }

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _full_path(self, path: str) -> str:
        # Prevent path traversal
        clean = os.path.normpath("/" + path).lstrip("/")
        return os.path.join(self.root, clean)

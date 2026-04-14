"""
Object Storage — a MinIO-compatible local simulation for the Cloud Desktop
storage system.  Stores binary objects in a local directory tree.
"""

import datetime
import hashlib
import json
import os
import shutil
from typing import Optional


class ObjectStorage:
    """
    Flat-namespace object store that mirrors the S3/MinIO bucket+key model.
    Data is persisted as files under ``<root>/<bucket>/<key>``.
    """

    def __init__(self, root_dir: str):
        self.root = root_dir
        os.makedirs(self.root, exist_ok=True)

    # ------------------------------------------------------------------
    # Bucket operations
    # ------------------------------------------------------------------

    def create_bucket(self, bucket: str) -> dict:
        path = self._bucket_path(bucket)
        os.makedirs(path, exist_ok=True)
        return {"status": "ok", "bucket": bucket, "path": path}

    def delete_bucket(self, bucket: str, force: bool = False) -> dict:
        path = self._bucket_path(bucket)
        if not os.path.isdir(path):
            return {"status": "not_found", "bucket": bucket}
        if not force and os.listdir(path):
            raise RuntimeError(f"Bucket '{bucket}' is not empty. Use force=True to delete.")
        shutil.rmtree(path)
        return {"status": "deleted", "bucket": bucket}

    def list_buckets(self) -> list:
        if not os.path.isdir(self.root):
            return []
        return [d for d in os.listdir(self.root) if os.path.isdir(os.path.join(self.root, d))]

    # ------------------------------------------------------------------
    # Object operations
    # ------------------------------------------------------------------

    def put_object(self, bucket: str, key: str, data: bytes,
                   content_type: str = "application/octet-stream") -> dict:
        self.create_bucket(bucket)
        obj_path = self._object_path(bucket, key)
        os.makedirs(os.path.dirname(obj_path), exist_ok=True)
        with open(obj_path, "wb") as f:
            f.write(data)
        etag = hashlib.md5(data).hexdigest()
        meta = {
            "bucket": bucket,
            "key": key,
            "size": len(data),
            "etag": etag,
            "content_type": content_type,
            "last_modified": datetime.datetime.utcnow().isoformat() + "Z",
        }
        with open(obj_path + ".meta.json", "w", encoding="utf-8") as f:
            json.dump(meta, f)
        return meta

    def get_object(self, bucket: str, key: str) -> bytes:
        path = self._object_path(bucket, key)
        if not os.path.isfile(path):
            raise FileNotFoundError(f"Object not found: {bucket}/{key}")
        with open(path, "rb") as f:
            return f.read()

    def delete_object(self, bucket: str, key: str) -> dict:
        path = self._object_path(bucket, key)
        if not os.path.isfile(path):
            return {"status": "not_found", "bucket": bucket, "key": key}
        os.remove(path)
        meta_path = path + ".meta.json"
        if os.path.isfile(meta_path):
            os.remove(meta_path)
        return {"status": "deleted", "bucket": bucket, "key": key}

    def list_objects(self, bucket: str, prefix: str = "") -> list:
        bucket_path = self._bucket_path(bucket)
        if not os.path.isdir(bucket_path):
            return []
        result = []
        for dirpath, _, filenames in os.walk(bucket_path):
            for fname in filenames:
                if fname.endswith(".meta.json"):
                    continue
                full = os.path.join(dirpath, fname)
                rel = os.path.relpath(full, bucket_path)
                if rel.startswith(prefix):
                    result.append({"bucket": bucket, "key": rel, "size": os.path.getsize(full)})
        return result

    def head_object(self, bucket: str, key: str) -> Optional[dict]:
        meta_path = self._object_path(bucket, key) + ".meta.json"
        if not os.path.isfile(meta_path):
            return None
        with open(meta_path, "r", encoding="utf-8") as f:
            return json.load(f)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _bucket_path(self, bucket: str) -> str:
        return os.path.join(self.root, bucket)

    def _object_path(self, bucket: str, key: str) -> str:
        safe_key = key.lstrip("/")
        return os.path.join(self.root, bucket, safe_key)

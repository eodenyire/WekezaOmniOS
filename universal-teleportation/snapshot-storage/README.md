# snapshot-storage

## Purpose
Implements storage backends and indexing for snapshot persistence, caching, and retrieval.

## Key Modules
- `storage_manager.py`: Backend orchestration.
- `local_storage.py`, `s3_backend.py`: Concrete storage implementations.
- `distributed_cache.py`: Cache acceleration layer.
- `storage_index.py`: Snapshot metadata indexing.

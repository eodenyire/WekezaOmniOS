"""
WekezaOmniOS Distributed Cache
Phase 4: In-memory snapshot caching layer for fast repeated restores.

Provides a write-through cache in front of any StorageBackend so that
frequently-requested snapshots are served from memory rather than disk.
"""
import threading


class DistributedCache:
    """
    Thread-safe in-memory LRU-style cache for snapshot objects.

    In a real distributed deployment this would be backed by Redis or
    Memcached; for the Phase 4 prototype it is a simple dict with a
    configurable capacity limit.
    """

    def __init__(self, capacity: int = 50):
        self._store: dict = {}
        self._lock = threading.Lock()
        self._capacity = capacity
        self._hits = 0
        self._misses = 0

    def put(self, snapshot_id: str, data: bytes) -> None:
        """
        Store snapshot bytes under snapshot_id.

        If the cache is full the oldest entry is evicted.

        Args:
            snapshot_id: Unique snapshot identifier.
            data: Raw bytes of the snapshot archive.
        """
        with self._lock:
            if snapshot_id in self._store:
                del self._store[snapshot_id]
            elif len(self._store) >= self._capacity:
                # Evict the oldest entry (FIFO)
                oldest = next(iter(self._store))
                del self._store[oldest]
                print(f"[DistributedCache] Evicted snapshot '{oldest}'.")
            self._store[snapshot_id] = data
            print(f"[DistributedCache] Cached snapshot '{snapshot_id}' ({len(data)} bytes).")

    def get(self, snapshot_id: str):
        """
        Retrieve snapshot bytes by ID, or None if not cached.

        Args:
            snapshot_id: Unique snapshot identifier.

        Returns:
            bytes or None
        """
        with self._lock:
            data = self._store.get(snapshot_id)
            if data is not None:
                self._hits += 1
                print(f"[DistributedCache] Cache HIT for '{snapshot_id}'.")
            else:
                self._misses += 1
                print(f"[DistributedCache] Cache MISS for '{snapshot_id}'.")
            return data

    def invalidate(self, snapshot_id: str) -> bool:
        """Remove a snapshot from the cache."""
        with self._lock:
            if snapshot_id in self._store:
                del self._store[snapshot_id]
                print(f"[DistributedCache] Invalidated '{snapshot_id}'.")
                return True
            return False

    def stats(self) -> dict:
        """Return cache hit/miss statistics."""
        total = self._hits + self._misses
        ratio = self._hits / total if total else 0.0
        return {
            "hits": self._hits,
            "misses": self._misses,
            "hit_ratio": round(ratio, 3),
            "size": len(self._store),
            "capacity": self._capacity,
        }

    def list_cached(self) -> list:
        """Return all currently cached snapshot IDs."""
        with self._lock:
            return list(self._store.keys())

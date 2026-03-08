"""In-memory node metrics aggregation for Phase 2."""

from datetime import datetime


class NodeMetrics:
    def __init__(self):
        self.teleportations = 0
        self.transfers_ok = 0
        self.transfers_failed = 0
        self.last_event = None

    def record_teleport(self, success=True):
        self.teleportations += 1
        if success:
            self.transfers_ok += 1
        else:
            self.transfers_failed += 1
        self.last_event = datetime.utcnow().isoformat() + "Z"

    def snapshot(self):
        return {
            "teleportations": self.teleportations,
            "transfers_ok": self.transfers_ok,
            "transfers_failed": self.transfers_failed,
            "last_event": self.last_event,
        }

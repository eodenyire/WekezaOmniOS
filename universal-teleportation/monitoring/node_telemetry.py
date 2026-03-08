"""
WekezaOmniOS Node Telemetry
Phase 8+: Collects and reports fine-grained telemetry for teleportation nodes.
"""Node telemetry event logging for Phase 2."""

import json
import os
from datetime import datetime


class NodeTelemetry:
	def __init__(self, telemetry_file="logs/node_telemetry.jsonl"):
		self.telemetry_file = telemetry_file
		os.makedirs(os.path.dirname(telemetry_file), exist_ok=True)

	def emit(self, event_type, payload):
		event = {
			"ts": datetime.utcnow().isoformat() + "Z",
			"event": event_type,
			"payload": payload,
		}
		with open(self.telemetry_file, "a", encoding="utf-8") as f:
			f.write(json.dumps(event) + "\n")
		return event

	def read_recent(self, max_lines=100):
		if not os.path.exists(self.telemetry_file):
			return []
		with open(self.telemetry_file, "r", encoding="utf-8") as f:
			lines = f.readlines()[-max_lines:]
		out = []
		for line in lines:
			line = line.strip()
			if not line:
				continue
			try:
				out.append(json.loads(line))
			except json.JSONDecodeError:
				continue
		return out

Telemetry data includes:
  - CPU / memory utilisation
  - Teleportation throughput (MB/s)
  - Success/failure rates
  - Active connection count
"""
from datetime import datetime, timezone
from typing import Dict, List, Optional
import time


class TelemetryRecord:
    """A single telemetry sample for a node."""

    def __init__(
        self,
        node_id: str,
        cpu_pct: float,
        memory_pct: float,
        throughput_mbps: float,
        active_connections: int,
        teleport_success: int = 0,
        teleport_failure: int = 0,
    ):
        self.node_id = node_id
        self.cpu_pct = cpu_pct
        self.memory_pct = memory_pct
        self.throughput_mbps = throughput_mbps
        self.active_connections = active_connections
        self.teleport_success = teleport_success
        self.teleport_failure = teleport_failure
        self.timestamp = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> dict:
        total = self.teleport_success + self.teleport_failure
        success_rate = (self.teleport_success / total) if total else 1.0
        return {
            "node_id": self.node_id,
            "timestamp": self.timestamp,
            "cpu_pct": round(self.cpu_pct, 2),
            "memory_pct": round(self.memory_pct, 2),
            "throughput_mbps": round(self.throughput_mbps, 2),
            "active_connections": self.active_connections,
            "teleport_success": self.teleport_success,
            "teleport_failure": self.teleport_failure,
            "success_rate": round(success_rate, 4),
        }


class NodeTelemetry:
    """
    Collects and aggregates telemetry samples for a specific node.
    """

    def __init__(self, node_id: str, max_history: int = 1000):
        self.node_id = node_id
        self.max_history = max_history
        self._samples: List[TelemetryRecord] = []

    def record(
        self,
        cpu_pct: float,
        memory_pct: float,
        throughput_mbps: float = 0.0,
        active_connections: int = 0,
        teleport_success: int = 0,
        teleport_failure: int = 0,
    ) -> TelemetryRecord:
        """
        Record a new telemetry sample.

        Returns:
            The recorded TelemetryRecord.
        """
        sample = TelemetryRecord(
            node_id=self.node_id,
            cpu_pct=cpu_pct,
            memory_pct=memory_pct,
            throughput_mbps=throughput_mbps,
            active_connections=active_connections,
            teleport_success=teleport_success,
            teleport_failure=teleport_failure,
        )
        self._samples.append(sample)
        # Evict oldest samples when over capacity
        if len(self._samples) > self.max_history:
            self._samples = self._samples[-self.max_history:]
        return sample

    def latest(self) -> Optional[TelemetryRecord]:
        """Return the most recent sample, or None if no samples recorded."""
        return self._samples[-1] if self._samples else None

    def average(self, last_n: int = 10) -> dict:
        """
        Compute average metrics over the last *last_n* samples.

        Returns:
            dict with averaged metric values.
        """
        window = self._samples[-last_n:]
        if not window:
            return {}
        count = len(window)
        return {
            "node_id": self.node_id,
            "sample_count": count,
            "avg_cpu_pct": round(sum(s.cpu_pct for s in window) / count, 2),
            "avg_memory_pct": round(sum(s.memory_pct for s in window) / count, 2),
            "avg_throughput_mbps": round(sum(s.throughput_mbps for s in window) / count, 2),
            "total_teleport_success": sum(s.teleport_success for s in window),
            "total_teleport_failure": sum(s.teleport_failure for s in window),
        }

    def history(self) -> List[dict]:
        """Return all recorded samples as dicts."""
        return [s.to_dict() for s in self._samples]

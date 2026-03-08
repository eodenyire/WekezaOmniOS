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


# 📄 telemetry_hub.py
# The "Hub" is designed to aggregate these metrics. In Phase 2, this file will be responsible for sending this data to your Central Dashboard or the Cluster Manager.

"""
WekezaOmniOS Telemetry Hub
Aggregates logs and metrics for external reporting.
"""

import json
from datetime import datetime

class TelemetryHub:
    def __init__(self):
        self.events = []

    def log_event(self, module, event_type, message):
        """Records a teleportation lifecycle event."""
        event = {
            "timestamp": datetime.now().isoformat(),
            "module": module,
            "type": event_type,
            "message": message
        }
        self.events.append(event)
        # In Phase 1, we simply print to console; Phase 2 will push to a database
        print(f"[Telemetry] {event['timestamp']} | {module} | {event_type} | {message}")

    def export_telemetry(self, file_path="logs/telemetry_report.json"):
        """Exports the current session's events to a JSON file."""
        with open(file_path, "w") as f:
            json.dump(self.events, f, indent=4)
        print(f"[Telemetry] Report exported to {file_path}")

hub = TelemetryHub() # Singleton instance for the engine

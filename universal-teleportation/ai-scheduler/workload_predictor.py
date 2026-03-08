"""
WekezaOmniOS Workload Predictor
Phase 9: Predicts the resource requirements of a teleportation workload
         to enable intelligent node selection and capacity planning.

The predictor uses a lightweight heuristic model that can be replaced with
a proper ML model (scikit-learn, TensorFlow Lite, etc.) in production.
"""
import math
from datetime import datetime, timezone


class WorkloadPredictor:
    """
    Analyses historical teleportation telemetry and predicts future
    resource requirements for workloads.
    """

    def __init__(self):
        self._history: list = []

    # ------------------------------------------------------------------
    # Telemetry ingestion
    # ------------------------------------------------------------------

    def record_teleportation(self, event: dict) -> None:
        """
        Record a completed teleportation event for future predictions.

        Args:
            event: dict with keys: process_id, memory_mb, cpu_cores,
                   duration_s, target_os, snapshot_size_kb.
        """
        event["recorded_at"] = datetime.now(timezone.utc).isoformat()
        self._history.append(event)

    # ------------------------------------------------------------------
    # Prediction
    # ------------------------------------------------------------------

    def predict_resources(self, snapshot_size_kb: int, target_os: str = "linux") -> dict:
        """
        Estimate the CPU cores and memory (MB) required to restore a workload.

        The heuristic:
          - base_memory = sqrt(snapshot_size_kb) * 0.5  (MB)
          - base_cpu    = max(1, snapshot_size_kb // 10000)
          - Windows adds 20% overhead; Android adds 15%.

        Args:
            snapshot_size_kb: Size of the snapshot archive in KB.
            target_os: Target operating system.

        Returns:
            dict with 'estimated_memory_mb', 'estimated_cpu_cores',
                      'estimated_transfer_s', 'confidence'.
        """
        base_memory = max(64, math.sqrt(snapshot_size_kb) * 0.5)
        base_cpu = max(1, snapshot_size_kb // 10_000)
        transfer_s = snapshot_size_kb / 10_000  # Assume 10 MB/s

        # OS overhead multipliers
        os_multipliers = {
            "windows": 1.20,
            "android": 1.15,
            "macos": 1.10,
            "ios": 1.10,
            "linux": 1.00,
        }
        multiplier = os_multipliers.get(target_os.lower(), 1.05)

        estimated_memory = round(base_memory * multiplier, 1)
        estimated_cpu = max(1, round(base_cpu * multiplier))
        confidence = min(0.95, 0.70 + len(self._history) * 0.01)

        prediction = {
            "estimated_memory_mb": estimated_memory,
            "estimated_cpu_cores": estimated_cpu,
            "estimated_transfer_s": round(transfer_s, 2),
            "target_os": target_os,
            "confidence": round(confidence, 3),
        }
        print(
            f"[WorkloadPredictor] Prediction for {target_os}: "
            f"{estimated_memory} MB RAM, {estimated_cpu} vCPU "
            f"(confidence {confidence:.1%})"
        )
        return prediction

    def average_transfer_time(self) -> float:
        """Return the average transfer duration from recorded history (seconds)."""
        if not self._history:
            return 0.0
        durations = [e.get("duration_s", 0) for e in self._history]
        return sum(durations) / len(durations)

    def history(self) -> list:
        """Return all recorded teleportation events."""
        return list(self._history)

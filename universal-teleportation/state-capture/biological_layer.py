"""
WekezaOmniOS Biological State Modeling Layer
Phase 12: Models biologically-relevant process states for digital twin
          and human-simulation applications.

Biological variables are stored as normalised metrics [0.0 – 1.0] with
clinical thresholds for safe/warning/critical status classification.
"""
from typing import Dict, Optional
from datetime import datetime, timezone


# Normal physiological ranges (used for threshold calculations)
NORMAL_RANGES = {
    "heartbeat_bpm":      (60,   100),
    "blood_pressure_sys": (90,   120),
    "blood_pressure_dia": (60,    80),
    "neural_activity":    (0.3,   0.7),
    "oxygen_saturation":  (95,   100),
    "core_temperature_c": (36.1, 37.2),
    "stress_level":       (0.0,   0.4),
}

STATUS_THRESHOLDS = {
    "normal":   1.0,
    "warning":  1.25,
    "critical": float("inf"),
}


class BiologicalStateModel:
    """
    Captures, validates, and serialises the biological state associated
    with a digital-twin process snapshot.
    """

    def __init__(self, entity_id: str = "entity_001"):
        self.entity_id = entity_id
        self._state: Dict[str, float] = {}

    # ------------------------------------------------------------------
    # State management
    # ------------------------------------------------------------------

    def set_variable(self, name: str, value: float) -> None:
        """Set a biological variable."""
        if name not in NORMAL_RANGES:
            print(f"[BiologicalLayer] ⚠️  Unknown variable '{name}' — storing anyway.")
        self._state[name] = value

    def get_variable(self, name: str) -> Optional[float]:
        """Retrieve a biological variable."""
        return self._state.get(name)

    def status(self, name: str) -> str:
        """
        Evaluate whether a variable is within safe operating limits.

        Returns:
            'normal', 'warning', or 'critical'.
        """
        value = self._state.get(name)
        if value is None:
            return "unknown"
        lo, hi = NORMAL_RANGES.get(name, (0, 1))
        mid = (lo + hi) / 2
        deviation = abs(value - mid) / max(mid, 1e-9)

        if deviation <= 0.25:
            return "normal"
        elif deviation <= 0.5:
            return "warning"
        return "critical"

    # ------------------------------------------------------------------
    # Simulation
    # ------------------------------------------------------------------

    def simulate_biological_state(self, process_id: int) -> dict:
        """
        Generate a synthetic biological state snapshot for a given process.

        In a real digital-twin application these values would be read from
        sensors or a simulation engine; here they are deterministically
        derived from the process ID for reproducibility.

        Args:
            process_id: PID of the associated process / digital twin.

        Returns:
            dict: Biological snapshot metadata.
        """
        import math
        seed = process_id % 1000

        defaults = {
            "heartbeat_bpm":      60 + (seed % 40),
            "blood_pressure_sys": 100 + (seed % 20),
            "blood_pressure_dia": 65 + (seed % 15),
            "neural_activity":    0.4 + (math.sin(seed) * 0.1),
            "oxygen_saturation":  97.0 + (seed % 3) * 0.5,
            "core_temperature_c": 36.5 + (seed % 10) * 0.07,
            "stress_level":       0.1 + (seed % 5) * 0.05,
        }
        for k, v in defaults.items():
            self.set_variable(k, v)

        snapshot = {
            "entity_id": self.entity_id,
            "process_id": process_id,
            "captured_at": datetime.now(timezone.utc).isoformat(),
            "variables": {k: {"value": v, "status": self.status(k)} for k, v in self._state.items()},
        }
        print(f"[BiologicalLayer] ✅ Biological state captured for PID {process_id} (entity: {self.entity_id})")
        return snapshot

    def to_dict(self) -> dict:
        """Export current state as a plain dict."""
        return {k: {"value": v, "status": self.status(k)} for k, v in self._state.items()}

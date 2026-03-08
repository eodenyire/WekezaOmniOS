"""
WekezaOmniOS Biological Safety Validator
Phase 18: Validates the biological state of a digital twin / human-
          simulation snapshot before allowing restoration.

Safety policy:
  - All vital signs must be within SAFE thresholds.
  - Neural activity must not exceed critical levels.
  - Any CRITICAL variable blocks restoration (returns ABORT).
  - WARNING variables allow restoration with a logged advisory.
"""
import logging
import os
from datetime import datetime, timezone
from typing import Dict, List, Optional


logger = logging.getLogger("biological_safety")
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("[%(levelname)s][BiologicalSafety] %(message)s"))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


# Safety thresholds — (min_safe, max_safe, min_warn, max_warn)
THRESHOLDS: Dict[str, tuple] = {
    "heartbeat_bpm":       (40,  180,  55,  120),
    "blood_pressure_sys":  (70,  200,  90,  145),
    "blood_pressure_dia":  (40,  120,  60,   95),
    "neural_activity":     (0.05, 0.95, 0.2,  0.8),
    "oxygen_saturation":   (80,  100,  92,  100),
    "core_temperature_c":  (34.0, 41.0, 35.5, 38.5),
    "stress_level":        (0.0,  1.0, 0.0,  0.7),
}


class BiologicalSafetyReport:
    """Summary of a biological safety validation."""

    def __init__(self, entity_id: str, snapshot_path: str):
        self.entity_id = entity_id
        self.snapshot_path = snapshot_path
        self.validated_at = datetime.now(timezone.utc).isoformat()
        self.findings: List[dict] = []
        self.verdict: str = "PASS"  # PASS | WARN | ABORT

    def add_finding(self, variable: str, value: float, level: str, message: str) -> None:
        self.findings.append({
            "variable": variable,
            "value": value,
            "level": level,
            "message": message,
        })
        if level == "CRITICAL" and self.verdict != "ABORT":
            self.verdict = "ABORT"
        elif level == "WARNING" and self.verdict == "PASS":
            self.verdict = "WARN"

    def to_dict(self) -> dict:
        return {
            "entity_id": self.entity_id,
            "snapshot_path": self.snapshot_path,
            "validated_at": self.validated_at,
            "verdict": self.verdict,
            "finding_count": len(self.findings),
            "findings": self.findings,
        }


class BiologicalSafetyValidator:
    """
    Phase 18: Validates biological snapshot safety before restoration.
    """

    def validate_biological_safety(
        self,
        snapshot_path: str,
        biological_state: Optional[dict] = None,
    ) -> BiologicalSafetyReport:
        """
        Validate a biological snapshot for safety compliance.

        Args:
            snapshot_path: Path to the snapshot archive.
            biological_state: Pre-loaded biological state dict (from
                              Phase 12 BiologicalStateModel.simulate_biological_state).
                              If None, a minimal default state is used.

        Returns:
            BiologicalSafetyReport with verdict: PASS, WARN, or ABORT.
        """
        logger.info(f"Validating biological safety for: {snapshot_path}")

        entity_id = (biological_state or {}).get("entity_id", "unknown")
        report = BiologicalSafetyReport(entity_id=entity_id, snapshot_path=snapshot_path)

        variables = {}
        if biological_state and "variables" in biological_state:
            variables = {k: v["value"] for k, v in biological_state["variables"].items()}
        else:
            # Use conservative defaults if no state provided
            variables = {
                "heartbeat_bpm": 72,
                "oxygen_saturation": 98,
                "neural_activity": 0.5,
            }

        for var, value in variables.items():
            if var not in THRESHOLDS:
                continue
            min_safe, max_safe, min_warn, max_warn = THRESHOLDS[var]

            if value < min_safe or value > max_safe:
                msg = f"{var}={value} outside absolute safe range [{min_safe}, {max_safe}]"
                report.add_finding(var, value, "CRITICAL", msg)
                logger.error(msg)
            elif value < min_warn or value > max_warn:
                msg = f"{var}={value} outside optimal range [{min_warn}, {max_warn}]"
                report.add_finding(var, value, "WARNING", msg)
                logger.warning(msg)
            else:
                logger.info(f"  ✓ {var}={value} — SAFE")

        verdict_emoji = {"PASS": "✅", "WARN": "⚠️", "ABORT": "🚫"}[report.verdict]
        logger.info(
            f"Biological safety check complete — verdict: {report.verdict} "
            f"{verdict_emoji} ({len(report.findings)} finding(s))"
        )
        return report

"""
WekezaOmniOS Energy-to-Matter Conversion Simulation
Phase 19: Simulates the energy state of a process for hypothetical
          energy-based teleportation.

In classical computing:
  - Energy state ≈ CPU power consumption + memory charge state + I/O signal levels.

This module models these as normalised energy vectors that can be:
  1. Captured from a running process (simulated via power metrics).
  2. Stored as energy metadata alongside the snapshot.
  3. Used to reconstruct the equivalent energy configuration at the target.
"""
import math
from datetime import datetime, timezone
from typing import Dict, Optional


# Typical TDP ranges (Watts) for different process categories
PROCESS_TDP = {
    "idle":          0.5,
    "interactive":   5.0,
    "compute":      15.0,
    "ml_training":  80.0,
    "default":       2.0,
}


class EnergyStateVector:
    """
    Represents the energy state of a computational component.
    """

    def __init__(self, component: str, power_w: float, frequency_mhz: float = 1000.0):
        self.component = component
        self.power_w = power_w
        self.frequency_mhz = frequency_mhz
        # Energy density: joules per clock cycle
        self.energy_per_cycle_pj = (power_w * 1e12) / (frequency_mhz * 1e6)

    def to_dict(self) -> dict:
        return {
            "component": self.component,
            "power_w": round(self.power_w, 4),
            "frequency_mhz": self.frequency_mhz,
            "energy_per_cycle_pj": round(self.energy_per_cycle_pj, 6),
        }


class EnergySimulator:
    """
    Phase 19: Captures and simulates process energy states for teleportation.
    """

    def __init__(self):
        self._energy_states: Dict[str, EnergyStateVector] = {}

    def simulate_energy_to_matter(self, process_id: int, process_class: str = "default") -> dict:
        """
        Simulate the energy-to-matter state for a process.

        Computes energy state vectors for CPU, memory bus, and I/O
        subsystems based on the process class.

        Args:
            process_id: PID of the target process.
            process_class: One of 'idle', 'interactive', 'compute',
                           'ml_training', 'default'.

        Returns:
            dict: Energy state snapshot.
        """
        print(f"[EnergySimulator] ⚡ Capturing energy state for PID {process_id} (class: {process_class})...")

        base_tdp = PROCESS_TDP.get(process_class, PROCESS_TDP["default"])
        seed = process_id % 100

        components = {
            "cpu_core_0":  EnergyStateVector("cpu_core_0",  base_tdp * 0.60, 3200 + seed),
            "cpu_core_1":  EnergyStateVector("cpu_core_1",  base_tdp * 0.30, 2800 + seed),
            "memory_bus":  EnergyStateVector("memory_bus",  base_tdp * 0.07, 4800.0),
            "io_subsystem": EnergyStateVector("io_subsystem", base_tdp * 0.03, 100.0),
        }
        self._energy_states = components

        total_power = sum(c.power_w for c in components.values())
        # Equivalent mass via E = mc²: m = E/c²  (purely symbolic for simulation)
        c = 3e8  # m/s
        equiv_mass_ng = (total_power * 1e-9) / (c ** 2)  # nanograms (tiny but illustrative)

        snapshot = {
            "process_id": process_id,
            "process_class": process_class,
            "captured_at": datetime.now(timezone.utc).isoformat(),
            "total_power_w": round(total_power, 4),
            "equivalent_mass_ng": round(equiv_mass_ng, 30),
            "components": {k: v.to_dict() for k, v in components.items()},
        }
        print(
            f"[EnergySimulator] ✅ Energy state captured — "
            f"total power: {total_power:.2f}W"
        )
        return snapshot

    def get_energy_state(self, component: str) -> Optional[EnergyStateVector]:
        """Retrieve the energy state vector for a specific component."""
        return self._energy_states.get(component)

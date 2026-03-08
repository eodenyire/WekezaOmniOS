"""
WekezaOmniOS Phase 19 Tests — Energy-to-Matter Conversion Simulation
"""
import pytest
from snapshot_engine.energy_simulation import EnergySimulator, EnergyStateVector, PROCESS_TDP


def test_energy_simulator_instantiation():
    simulator = EnergySimulator()
    assert simulator is not None


def test_energy_state_vector():
    esv = EnergyStateVector("cpu_core_0", power_w=15.0, frequency_mhz=3200)
    assert esv.power_w == 15.0
    assert esv.energy_per_cycle_pj > 0


def test_simulate_returns_snapshot():
    simulator = EnergySimulator()
    result = simulator.simulate_energy_to_matter(process_id=500)
    assert result["process_id"] == 500
    assert "total_power_w" in result
    assert "components" in result


def test_simulate_all_components_present():
    simulator = EnergySimulator()
    result = simulator.simulate_energy_to_matter(process_id=1)
    components = result["components"]
    for name in ("cpu_core_0", "cpu_core_1", "memory_bus", "io_subsystem"):
        assert name in components


def test_total_power_positive():
    simulator = EnergySimulator()
    result = simulator.simulate_energy_to_matter(process_id=42)
    assert result["total_power_w"] > 0


def test_compute_class_higher_power_than_idle():
    simulator = EnergySimulator()
    idle = simulator.simulate_energy_to_matter(process_id=1, process_class="idle")
    compute = simulator.simulate_energy_to_matter(process_id=1, process_class="compute")
    assert compute["total_power_w"] > idle["total_power_w"]


def test_get_energy_state():
    simulator = EnergySimulator()
    simulator.simulate_energy_to_matter(process_id=99)
    esv = simulator.get_energy_state("cpu_core_0")
    assert esv is not None
    assert esv.power_w > 0


def test_component_to_dict():
    esv = EnergyStateVector("test_comp", power_w=5.0)
    d = esv.to_dict()
    assert d["component"] == "test_comp"
    assert d["power_w"] == 5.0

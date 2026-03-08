"""
WekezaOmniOS Phase 11 Tests — Quantum State Simulation
"""
import pytest
from state_capture.quantum_layer import QuantumLayer, QuantumStateVector


def test_state_vector_instantiation():
    sv = QuantumStateVector("reg_eax", num_qubits=4)
    assert len(sv.amplitudes) == 16


def test_state_vector_collapse_returns_valid_index():
    sv = QuantumStateVector("reg_ebx", num_qubits=4)
    result = sv.collapse()
    assert 0 <= result < 16


def test_state_vector_to_dict():
    sv = QuantumStateVector("reg_ecx", num_qubits=4)
    sv.collapse()
    d = sv.to_dict()
    assert d["label"] == "reg_ecx"
    assert "classical_value" in d


def test_quantum_layer_simulate():
    ql = QuantumLayer()
    meta = ql.simulate_quantum_state(process_id=1234)
    assert meta["process_id"] == 1234
    assert "registers" in meta
    assert 0.9 <= meta["fidelity_estimate"] <= 1.0


def test_quantum_layer_all_registers_captured():
    ql = QuantumLayer()
    meta = ql.simulate_quantum_state(process_id=42)
    for reg in QuantumLayer.REGISTERS:
        assert reg in meta["registers"]


def test_quantum_layer_entanglement_recorded():
    ql = QuantumLayer()
    meta = ql.simulate_quantum_state(process_id=99)
    assert ["eax", "ebx"] in meta["entangled_pairs"]

"""
WekezaOmniOS Phase 20 Tests — Teleportation Hardware Interface
"""
import time
import pytest
from transfer_layer.hardware_interface import HardwareInterface, HardwareTransferStatus


def test_hardware_interface_instantiation():
    hw = HardwareInterface()
    assert hw is not None
    assert hw.is_online() is True


def test_device_info():
    hw = HardwareInterface()
    info = hw.device_info()
    assert info["status"] == "ONLINE"
    assert "protocol_version" in info


def test_initiate_transfer(tmp_path):
    snap = tmp_path / "snap.tar.gz"
    snap.write_bytes(b"payload")
    hw = HardwareInterface(simulate_duration_s=0.05)
    result = hw.initiate_hardware_transfer(str(snap), "hw-node-01")
    assert "transfer_id" in result
    # status is either QUEUED or ENCODING depending on thread scheduling
    assert result["status"] in (HardwareTransferStatus.QUEUED, HardwareTransferStatus.ENCODING)


def test_transfer_completes(tmp_path):
    snap = tmp_path / "snap.tar.gz"
    snap.write_bytes(b"payload")
    hw = HardwareInterface(simulate_duration_s=0.1)
    result = hw.initiate_hardware_transfer(str(snap), "hw-node-02")
    transfer_id = result["transfer_id"]
    time.sleep(0.2)  # Wait for background thread
    status = hw.monitor_hardware_status(transfer_id)
    assert status["status"] == HardwareTransferStatus.COMPLETE
    assert status["progress_pct"] == 100.0


def test_abort_transfer(tmp_path):
    snap = tmp_path / "snap.tar.gz"
    snap.write_bytes(b"payload")
    hw = HardwareInterface(simulate_duration_s=5.0)  # Slow to allow abort
    result = hw.initiate_hardware_transfer(str(snap), "hw-node-03")
    transfer_id = result["transfer_id"]
    aborted = hw.abort_hardware_transfer(transfer_id)
    assert aborted is True
    status = hw.monitor_hardware_status(transfer_id)
    assert status["status"] == HardwareTransferStatus.ABORTED


def test_abort_completed_returns_false(tmp_path):
    snap = tmp_path / "snap.tar.gz"
    snap.write_bytes(b"payload")
    hw = HardwareInterface(simulate_duration_s=0.05)
    result = hw.initiate_hardware_transfer(str(snap), "hw-node-04")
    time.sleep(0.2)
    aborted = hw.abort_hardware_transfer(result["transfer_id"])
    assert aborted is False


def test_monitor_unknown_transfer():
    hw = HardwareInterface()
    result = hw.monitor_hardware_status("nonexistent-id")
    assert "error" in result


def test_list_transfers(tmp_path):
    snap = tmp_path / "snap.tar.gz"
    snap.write_bytes(b"data")
    hw = HardwareInterface(simulate_duration_s=0.05)
    hw.initiate_hardware_transfer(str(snap), "node-a")
    hw.initiate_hardware_transfer(str(snap), "node-b")
    transfers = hw.list_transfers()
    assert len(transfers) == 2


def test_send_to_hardware_alias(tmp_path):
    snap = tmp_path / "snap.tar.gz"
    snap.write_bytes(b"data")
    hw = HardwareInterface(simulate_duration_s=0.05)
    result = hw.send_to_hardware(str(snap))
    assert "transfer_id" in result

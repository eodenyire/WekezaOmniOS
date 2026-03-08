"""
WekezaOmniOS Teleportation Hardware Interface
Phase 20: Abstraction layer between the software teleportation engine and
          future physical teleportation hardware devices.

API contract:
  - initiate_hardware_transfer(snapshot_path, target_device) -> dict
  - monitor_hardware_status(transfer_id) -> dict
  - abort_hardware_transfer(transfer_id) -> bool

The protocol simulates a hardware device that:
  1. Accepts a snapshot payload.
  2. Performs matter-energy encoding (simulated).
  3. Transmits the encoded payload to the target.
  4. Signals completion or error.
"""
import uuid
import time
import threading
from datetime import datetime, timezone
from typing import Dict, Optional


class HardwareTransferStatus:
    """Transfer status constants."""
    QUEUED = "QUEUED"
    ENCODING = "ENCODING"
    TRANSMITTING = "TRANSMITTING"
    COMPLETE = "COMPLETE"
    ABORTED = "ABORTED"
    ERROR = "ERROR"


class HardwareTransferRecord:
    """Tracks the state of a single hardware transfer."""

    def __init__(self, transfer_id: str, snapshot_path: str, target_device: str):
        self.transfer_id = transfer_id
        self.snapshot_path = snapshot_path
        self.target_device = target_device
        self.status = HardwareTransferStatus.QUEUED
        self.progress_pct: float = 0.0
        self.created_at = datetime.now(timezone.utc).isoformat()
        self.completed_at: Optional[str] = None
        self.error: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "transfer_id": self.transfer_id,
            "snapshot_path": self.snapshot_path,
            "target_device": self.target_device,
            "status": self.status,
            "progress_pct": round(self.progress_pct, 1),
            "created_at": self.created_at,
            "completed_at": self.completed_at,
            "error": self.error,
        }


class HardwareInterface:
    """
    Phase 20: Software abstraction layer for teleportation hardware devices.

    In production this would communicate with a hardware driver over PCIe,
    USB, or a proprietary bus. Here the device behaviour is simulated
    asynchronously using a background thread.
    """

    def __init__(self, device_id: str = "UAT-HW-001", simulate_duration_s: float = 0.1):
        """
        Args:
            device_id: Identifier of the physical hardware device.
            simulate_duration_s: Duration of the simulated encoding/transmit
                                 cycle (kept short for test speed).
        """
        self.device_id = device_id
        self.simulate_duration_s = simulate_duration_s
        self._transfers: Dict[str, HardwareTransferRecord] = {}
        self._device_online = True

    # ------------------------------------------------------------------
    # Device control
    # ------------------------------------------------------------------

    def is_online(self) -> bool:
        """Return True if the hardware device is reachable."""
        return self._device_online

    def device_info(self) -> dict:
        """Return hardware device metadata."""
        return {
            "device_id": self.device_id,
            "status": "ONLINE" if self._device_online else "OFFLINE",
            "protocol_version": "UAT/2.0",
            "max_payload_gb": 1024,
        }

    # ------------------------------------------------------------------
    # Transfer operations
    # ------------------------------------------------------------------

    def initiate_hardware_transfer(
        self, snapshot_path: str, target_device: str
    ) -> dict:
        """
        Initiate a hardware-assisted snapshot transfer.

        Args:
            snapshot_path: Path to the snapshot archive.
            target_device: Identifier of the target hardware endpoint.

        Returns:
            dict with transfer_id and initial status.
        """
        if not self._device_online:
            return {"status": HardwareTransferStatus.ERROR, "reason": "Device offline"}

        transfer_id = f"htx-{uuid.uuid4().hex[:8]}"
        record = HardwareTransferRecord(transfer_id, snapshot_path, target_device)
        self._transfers[transfer_id] = record

        print(f"[HardwareInterface] 🔌 Initiating hardware transfer {transfer_id}")
        print(f"[HardwareInterface]    {snapshot_path} -> {target_device}")

        # Run the simulated transfer pipeline in background
        thread = threading.Thread(
            target=self._run_transfer_pipeline, args=(transfer_id,), daemon=True
        )
        thread.start()

        return {"transfer_id": transfer_id, "status": record.status}

    def _run_transfer_pipeline(self, transfer_id: str) -> None:
        """Simulate the hardware encoding → transmit → complete pipeline."""
        record = self._transfers[transfer_id]
        step_duration = self.simulate_duration_s / 3

        # Stage 1: Encoding
        record.status = HardwareTransferStatus.ENCODING
        record.progress_pct = 0.0
        time.sleep(step_duration)
        record.progress_pct = 33.0

        # Stage 2: Transmitting
        record.status = HardwareTransferStatus.TRANSMITTING
        time.sleep(step_duration)
        record.progress_pct = 66.0

        # Stage 3: Complete
        time.sleep(step_duration)
        record.progress_pct = 100.0
        record.status = HardwareTransferStatus.COMPLETE
        record.completed_at = datetime.now(timezone.utc).isoformat()
        print(f"[HardwareInterface] ✅ Transfer {transfer_id} complete.")

    def monitor_hardware_status(self, transfer_id: str) -> dict:
        """
        Return the current status of a hardware transfer.

        Args:
            transfer_id: ID returned by initiate_hardware_transfer.

        Returns:
            dict with status, progress, and timestamps.
        """
        record = self._transfers.get(transfer_id)
        if record is None:
            return {"error": f"Transfer '{transfer_id}' not found"}
        return record.to_dict()

    def abort_hardware_transfer(self, transfer_id: str) -> bool:
        """
        Abort an in-progress hardware transfer.

        Args:
            transfer_id: Transfer to abort.

        Returns:
            bool: True if aborted, False if already complete or not found.
        """
        record = self._transfers.get(transfer_id)
        if record is None:
            return False
        if record.status in (HardwareTransferStatus.COMPLETE, HardwareTransferStatus.ABORTED):
            return False
        record.status = HardwareTransferStatus.ABORTED
        record.error = "Aborted by operator"
        print(f"[HardwareInterface] ⛔ Transfer {transfer_id} aborted.")
        return True

    def list_transfers(self) -> list:
        """Return all transfer records."""
        return [r.to_dict() for r in self._transfers.values()]

    def send_to_hardware(self, snapshot_path: str, target_device: str = "default") -> dict:
        """Convenience alias for initiate_hardware_transfer."""
        return self.initiate_hardware_transfer(snapshot_path, target_device)

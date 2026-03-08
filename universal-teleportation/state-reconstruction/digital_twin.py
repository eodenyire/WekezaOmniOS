"""
WekezaOmniOS Digital Twin Cloning Engine
Phase 13: Creates and manages digital twins — persistent virtual replicas
          of running processes that can be independently evolved, tested,
          or teleported without affecting the original.

A digital twin is a stateful clone that:
  1. Shares the original snapshot as its seed state.
  2. Maintains independent runtime divergence tracking.
  3. Supports fork, merge, and comparison operations.
"""
import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional


class DigitalTwin:
    """
    A single digital twin instance derived from a parent snapshot.
    """

    def __init__(
        self,
        twin_id: str,
        parent_pid: int,
        snapshot_id: str,
        metadata: Optional[dict] = None,
    ):
        self.twin_id = twin_id
        self.parent_pid = parent_pid
        self.snapshot_id = snapshot_id
        self.metadata = metadata or {}
        self.created_at = datetime.now(timezone.utc).isoformat()
        self.status = "active"
        self._events: List[dict] = []

    def record_event(self, event_type: str, detail: str) -> None:
        """Log a lifecycle event for this twin."""
        self._events.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "type": event_type,
            "detail": detail,
        })

    def divergence_score(self) -> float:
        """
        Estimate how much this twin has diverged from the parent.
        Returns a value in [0.0, 1.0]; 0 = identical, 1 = fully diverged.
        """
        return min(1.0, len(self._events) * 0.05)

    def to_dict(self) -> dict:
        return {
            "twin_id": self.twin_id,
            "parent_pid": self.parent_pid,
            "snapshot_id": self.snapshot_id,
            "status": self.status,
            "created_at": self.created_at,
            "divergence_score": self.divergence_score(),
            "event_count": len(self._events),
            "metadata": self.metadata,
        }


class DigitalTwinEngine:
    """
    Phase 13: Orchestrates the creation, tracking, and lifecycle management
              of digital twins across a cluster.
    """

    def __init__(self):
        self._twins: Dict[str, DigitalTwin] = {}

    # ------------------------------------------------------------------
    # Creation
    # ------------------------------------------------------------------

    def create_digital_twin(
        self,
        process_id: int,
        snapshot_id: str,
        metadata: Optional[dict] = None,
    ) -> DigitalTwin:
        """
        Create a digital twin from a process snapshot.

        Args:
            process_id: PID of the original process.
            snapshot_id: Identifier of the captured snapshot.
            metadata: Optional extra context.

        Returns:
            DigitalTwin instance.
        """
        twin_id = f"twin-{uuid.uuid4().hex[:8]}"
        twin = DigitalTwin(
            twin_id=twin_id,
            parent_pid=process_id,
            snapshot_id=snapshot_id,
            metadata=metadata,
        )
        self._twins[twin_id] = twin
        twin.record_event("CREATED", f"Spawned from PID {process_id} snapshot {snapshot_id}")
        print(f"[DigitalTwinEngine] ✅ Twin '{twin_id}' created from PID {process_id}")
        return twin

    def fork_twin(self, twin_id: str) -> Optional[DigitalTwin]:
        """
        Fork an existing twin into a new independent twin.

        Args:
            twin_id: ID of the twin to fork.

        Returns:
            New DigitalTwin, or None if the source twin doesn't exist.
        """
        source = self._twins.get(twin_id)
        if source is None:
            print(f"[DigitalTwinEngine] ⚠️  Twin '{twin_id}' not found.")
            return None
        forked = self.create_digital_twin(
            source.parent_pid,
            source.snapshot_id,
            metadata={**source.metadata, "forked_from": twin_id},
        )
        forked.record_event("FORKED", f"Forked from twin '{twin_id}'")
        print(f"[DigitalTwinEngine] ✅ Forked twin '{twin_id}' -> '{forked.twin_id}'")
        return forked

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def terminate_twin(self, twin_id: str) -> bool:
        """Mark a twin as terminated."""
        twin = self._twins.get(twin_id)
        if twin:
            twin.status = "terminated"
            twin.record_event("TERMINATED", "Twin lifecycle ended")
            print(f"[DigitalTwinEngine] Twin '{twin_id}' terminated.")
            return True
        return False

    def get_twin(self, twin_id: str) -> Optional[DigitalTwin]:
        return self._twins.get(twin_id)

    def list_twins(self, status: Optional[str] = None) -> List[DigitalTwin]:
        """Return all twins, optionally filtered by status."""
        twins = list(self._twins.values())
        if status:
            twins = [t for t in twins if t.status == status]
        return twins

    def compare(self, twin_id_a: str, twin_id_b: str) -> dict:
        """
        Compare divergence between two twins sharing a common ancestor.

        Returns:
            dict with divergence scores and comparison summary.
        """
        a = self._twins.get(twin_id_a)
        b = self._twins.get(twin_id_b)
        if not a or not b:
            return {"error": "One or both twins not found"}
        return {
            "twin_a": twin_id_a,
            "twin_b": twin_id_b,
            "divergence_a": a.divergence_score(),
            "divergence_b": b.divergence_score(),
            "same_origin": a.snapshot_id == b.snapshot_id,
            "delta": abs(a.divergence_score() - b.divergence_score()),
        }

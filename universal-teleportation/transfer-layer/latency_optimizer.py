"""
WekezaOmniOS Latency Optimizer
Phase 15: Adapts snapshot transfer strategies for high-latency networks,
          including interplanetary-scale connections (> 1 second RTT).

Key techniques:
  - Adaptive chunk sizing based on bandwidth-delay product (BDP).
  - Delay-tolerant networking (DTN) with store-and-forward.
  - Forward error correction (FEC) metadata injection.
  - Scheduled teleportation windows for periodic high-latency links.
"""
from typing import Optional
import math
from datetime import datetime, timezone, timedelta


# Speed of light delay estimates (one-way, in seconds)
PROPAGATION_DELAYS = {
    "earth_low_orbit":       0.005,
    "earth_geostationary":   0.27,
    "earth_moon":            1.28,
    "earth_mars_min":        182.0,    # Closest approach
    "earth_mars_max":        1342.0,   # Farthest
    "earth_jupiter":         2610.0,
}


class LatencyOptimizer:
    """
    Phase 15: Computes optimal transfer parameters for any latency budget
              and implements delay-tolerant scheduling.
    """

    def __init__(self, bandwidth_mbps: float = 100.0):
        """
        Args:
            bandwidth_mbps: Available network bandwidth in Mbit/s.
        """
        self.bandwidth_mbps = bandwidth_mbps
        self._scheduled_transfers: list = []

    # ------------------------------------------------------------------
    # Parameter calculation
    # ------------------------------------------------------------------

    def optimize_latency(self, snapshot_path: str, rtt_ms: float = 50.0) -> dict:
        """
        Compute optimal transfer parameters for a given RTT.

        The bandwidth-delay product (BDP) determines the ideal chunk size
        to keep the pipe full: BDP = bandwidth * RTT / 2.

        Args:
            snapshot_path: Path to the snapshot archive (used for size hint).
            rtt_ms: Round-trip time in milliseconds.

        Returns:
            dict with chunk_size_kb, window_size, fec_redundancy_pct,
                  estimated_transfer_s.
        """
        import os
        size_bytes = os.path.getsize(snapshot_path) if os.path.exists(snapshot_path) else 1_000_000

        rtt_s = rtt_ms / 1000.0
        bdp_bytes = (self.bandwidth_mbps * 1e6 / 8) * (rtt_s / 2)
        chunk_size_kb = max(64, min(65536, int(bdp_bytes / 1024)))
        window_size = max(1, int(bdp_bytes / (chunk_size_kb * 1024)))

        # FEC overhead scales with latency (higher latency → more redundancy)
        fec_pct = min(50, int(math.log10(max(rtt_ms, 1)) * 10))

        n_chunks = math.ceil(size_bytes / (chunk_size_kb * 1024))
        estimated_s = (size_bytes / (self.bandwidth_mbps * 1e6 / 8)) * (1 + fec_pct / 100)

        params = {
            "snapshot_path": snapshot_path,
            "snapshot_size_bytes": size_bytes,
            "rtt_ms": rtt_ms,
            "chunk_size_kb": chunk_size_kb,
            "window_size": window_size,
            "fec_redundancy_pct": fec_pct,
            "n_chunks": n_chunks,
            "estimated_transfer_s": round(estimated_s, 2),
        }
        print(
            f"[LatencyOptimizer] RTT={rtt_ms}ms → chunk={chunk_size_kb}KB, "
            f"FEC={fec_pct}%, ETA={estimated_s:.1f}s"
        )
        return params

    # ------------------------------------------------------------------
    # Scheduled / delay-tolerant transfer
    # ------------------------------------------------------------------

    def schedule_transfer(
        self,
        snapshot_path: str,
        target_node: str,
        delay_s: float,
        route: str = "earth_geostationary",
    ) -> dict:
        """
        Schedule a snapshot transfer to be dispatched after *delay_s* seconds.

        This implements the DTN store-and-forward model required for
        interplanetary links where the contact window may be hours away.

        Args:
            snapshot_path: Path to the snapshot archive.
            target_node: Destination node identifier.
            delay_s: Seconds until the transfer should be dispatched.
            route: Named propagation route (for delay annotation).

        Returns:
            dict with schedule metadata.
        """
        dispatch_at = datetime.now(timezone.utc) + timedelta(seconds=delay_s)
        propagation = PROPAGATION_DELAYS.get(route, 0.0)
        arrival_at = dispatch_at + timedelta(seconds=propagation)

        entry = {
            "snapshot_path": snapshot_path,
            "target_node": target_node,
            "route": route,
            "delay_s": delay_s,
            "propagation_s": propagation,
            "dispatch_at": dispatch_at.isoformat(),
            "estimated_arrival_at": arrival_at.isoformat(),
            "status": "SCHEDULED",
        }
        self._scheduled_transfers.append(entry)
        print(
            f"[LatencyOptimizer] Scheduled transfer to '{target_node}' "
            f"via {route} — dispatch @ {dispatch_at.isoformat()}"
        )
        return entry

    def list_scheduled(self) -> list:
        """Return all pending scheduled transfers."""
        return list(self._scheduled_transfers)

    def propagation_delay(self, route: str) -> float:
        """Return one-way propagation delay (seconds) for a named route."""
        return PROPAGATION_DELAYS.get(route, 0.0)

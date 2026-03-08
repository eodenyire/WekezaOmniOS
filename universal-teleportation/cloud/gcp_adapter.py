"""
WekezaOmniOS GCP Cloud Adapter
Phase 8: Provisions and manages teleportation targets on Google Cloud Platform.

In production this uses google-cloud-compute and google-cloud-storage.
The prototype simulates GCP operations.
"""
import os
import uuid
from datetime import datetime, timezone


class GCPAdapter:
    """
    Adapter for teleporting workloads to GCP Compute Engine instances and
    storing snapshots in Google Cloud Storage.
    """

    def __init__(self, project: str = "wekeza-uat", zone: str = "us-central1-a", bucket: str = "uat-snapshots-gcp"):
        self.project = project
        self.zone = zone
        self.bucket = bucket
        self._instances: dict = {}

    def provision_node(self, machine_type: str = "n1-standard-2") -> dict:
        """Provision a GCE instance."""
        name = f"uat-node-{uuid.uuid4().hex[:6]}"
        ip = f"35.{os.getpid() % 256}.{len(self._instances)}.1"
        node = {
            "name": name,
            "machine_type": machine_type,
            "zone": self.zone,
            "project": self.project,
            "external_ip": ip,
            "status": "RUNNING",
            "provisioned_at": datetime.now(timezone.utc).isoformat(),
        }
        self._instances[name] = node
        print(f"[GCPAdapter] Provisioned GCE {name} ({machine_type}) @ {ip}")
        return node

    def delete_node(self, name: str) -> bool:
        """Delete a GCE instance."""
        if name in self._instances:
            self._instances[name]["status"] = "TERMINATED"
            print(f"[GCPAdapter] Deleted instance {name}.")
            return True
        return False

    def list_nodes(self) -> list:
        return list(self._instances.values())

    def upload_snapshot(self, snapshot_path: str, snapshot_id: str) -> str:
        """Upload snapshot to GCS."""
        gcs_uri = f"gs://{self.bucket}/snapshots/{snapshot_id}/{os.path.basename(snapshot_path)}"
        print(f"[GCPAdapter] Uploading {snapshot_path} -> {gcs_uri}")
        return gcs_uri

    def download_snapshot(self, snapshot_id: str, dest_path: str) -> str:
        """Download snapshot from GCS."""
        local_path = os.path.join(dest_path, f"{snapshot_id}.tar.gz")
        print(f"[GCPAdapter] Downloading gs://{self.bucket}/snapshots/{snapshot_id}/ -> {local_path}")
        return local_path

    def teleport(self, snapshot_path: str, machine_type: str = "n1-standard-2") -> dict:
        """End-to-end teleportation to GCP."""
        node = self.provision_node(machine_type)
        snapshot_id = f"snap-gcp-{uuid.uuid4().hex[:8]}"
        gcs_uri = self.upload_snapshot(snapshot_path, snapshot_id)
        print(f"[GCPAdapter] ✅ Teleportation to GCP complete — node {node['name']}")
        return {"node": node, "snapshot_id": snapshot_id, "gcs_uri": gcs_uri}

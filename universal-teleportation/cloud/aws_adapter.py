"""
WekezaOmniOS AWS Cloud Adapter
Phase 8: Provisions and manages teleportation targets on Amazon Web Services.

In production this would use boto3 to interact with EC2 and S3.
The prototype simulates cloud operations with local state tracking.
"""
import os
import uuid
from datetime import datetime, timezone


class AWSAdapter:
    """
    Adapter for teleporting workloads to AWS EC2 instances and
    storing snapshots in S3.
    """

    def __init__(self, region: str = "us-east-1", bucket: str = "uat-snapshots"):
        self.region = region
        self.bucket = bucket
        self._instances: dict = {}

    # ------------------------------------------------------------------
    # Node Provisioning
    # ------------------------------------------------------------------

    def provision_node(self, instance_type: str = "t3.medium") -> dict:
        """
        Provision a new EC2 instance for receiving a teleported workload.

        Args:
            instance_type: EC2 instance type.

        Returns:
            dict with instance metadata.
        """
        instance_id = f"i-{uuid.uuid4().hex[:8]}"
        public_ip = f"54.{os.getpid() % 256}.{len(self._instances)}.1"
        node = {
            "instance_id": instance_id,
            "instance_type": instance_type,
            "region": self.region,
            "public_ip": public_ip,
            "state": "running",
            "provisioned_at": datetime.now(timezone.utc).isoformat(),
        }
        self._instances[instance_id] = node
        print(f"[AWSAdapter] Provisioned EC2 {instance_id} ({instance_type}) @ {public_ip}")
        return node

    def terminate_node(self, instance_id: str) -> bool:
        """Terminate an EC2 instance."""
        if instance_id in self._instances:
            self._instances[instance_id]["state"] = "terminated"
            print(f"[AWSAdapter] Terminated instance {instance_id}.")
            return True
        print(f"[AWSAdapter] Instance {instance_id} not found.")
        return False

    def list_nodes(self) -> list:
        """Return all managed instances."""
        return list(self._instances.values())

    # ------------------------------------------------------------------
    # Snapshot Storage
    # ------------------------------------------------------------------

    def upload_snapshot(self, snapshot_path: str, snapshot_id: str) -> str:
        """
        Upload a snapshot archive to S3.

        Args:
            snapshot_path: Local path to the .tar.gz snapshot.
            snapshot_id: Unique identifier for the snapshot.

        Returns:
            S3 URI of the uploaded object.
        """
        s3_key = f"snapshots/{snapshot_id}/{os.path.basename(snapshot_path)}"
        s3_uri = f"s3://{self.bucket}/{s3_key}"
        print(f"[AWSAdapter] Uploading {snapshot_path} -> {s3_uri}")
        # In production: boto3.client('s3').upload_file(snapshot_path, self.bucket, s3_key)
        return s3_uri

    def download_snapshot(self, snapshot_id: str, dest_path: str) -> str:
        """
        Download a snapshot from S3.

        Args:
            snapshot_id: Snapshot identifier.
            dest_path: Local destination directory.

        Returns:
            Local path of the downloaded archive.
        """
        s3_key = f"snapshots/{snapshot_id}/snapshot.tar.gz"
        local_path = os.path.join(dest_path, f"{snapshot_id}.tar.gz")
        print(f"[AWSAdapter] Downloading s3://{self.bucket}/{s3_key} -> {local_path}")
        # In production: boto3.client('s3').download_file(self.bucket, s3_key, local_path)
        return local_path

    # ------------------------------------------------------------------
    # Teleportation
    # ------------------------------------------------------------------

    def teleport(self, snapshot_path: str, instance_type: str = "t3.medium") -> dict:
        """
        End-to-end teleportation to AWS:
        1. Provision a node.
        2. Upload snapshot to S3.
        3. Return node + snapshot metadata.

        Args:
            snapshot_path: Local snapshot archive.
            instance_type: EC2 instance type to provision.

        Returns:
            dict with node and snapshot details.
        """
        node = self.provision_node(instance_type)
        snapshot_id = f"snap-{uuid.uuid4().hex[:8]}"
        s3_uri = self.upload_snapshot(snapshot_path, snapshot_id)
        print(f"[AWSAdapter] ✅ Teleportation to AWS complete — node {node['instance_id']}")
        return {"node": node, "snapshot_id": snapshot_id, "s3_uri": s3_uri}

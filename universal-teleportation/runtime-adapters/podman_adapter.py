"""
WekezaOmniOS Podman Adapter
Phase 3: Integrates with the Podman container runtime for rootless teleportation.
"""
import subprocess


class PodmanAdapter:
    """
    Adapter for checkpoint/restore operations using Podman + CRIU.
    Supports rootless container teleportation.
    """

    def list_containers(self) -> list:
        """Return running Podman container IDs."""
        result = subprocess.run(
            ["podman", "ps", "--format", "{{.ID}}"],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print(f"[PodmanAdapter] Warning: {result.stderr.strip()}")
            return []
        return [cid for cid in result.stdout.strip().split("\n") if cid]

    def checkpoint_container(self, container_id: str, checkpoint_name: str = "uat-checkpoint") -> str:
        """
        Checkpoint a running Podman container using CRIU.

        Args:
            container_id: The Podman container ID.
            checkpoint_name: Label for the checkpoint archive.

        Returns:
            Path to the checkpoint archive.
        """
        archive_path = f"/tmp/{checkpoint_name}.tar.gz"
        result = subprocess.run(
            ["podman", "container", "checkpoint", container_id,
             "--export", archive_path],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print(f"[PodmanAdapter] Checkpoint failed: {result.stderr.strip()}")
        else:
            print(f"[PodmanAdapter] Checkpoint saved to {archive_path}")
        return archive_path

    def restore_container(self, archive_path: str) -> bool:
        """
        Restore a Podman container from a checkpoint archive.

        Args:
            archive_path: Path to the .tar.gz checkpoint archive.

        Returns:
            bool: True on success, False otherwise.
        """
        result = subprocess.run(
            ["podman", "container", "restore", "--import", archive_path],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print(f"[PodmanAdapter] Restore failed: {result.stderr.strip()}")
            return False
        print(f"[PodmanAdapter] Container restored from {archive_path}")
        return True

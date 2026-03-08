import subprocess

class DockerAdapter:
    """
    Adapter for interacting with Docker containers.
    """

    def is_available(self):
        result = subprocess.run(["which", "docker"], capture_output=True, text=True)
        return result.returncode == 0

    def list_containers(self):
        if not self.is_available():
            return []
        result = subprocess.run(
            ["docker", "ps", "--format", "{{.ID}}"],
            capture_output=True,
            text=True
        )
        output = result.stdout.strip()
        return output.split("\n") if output else []

    def inspect_container(self, container_id):
        if not self.is_available():
            return ""
        result = subprocess.run(
            ["docker", "inspect", container_id],
            capture_output=True,
            text=True
        )

        return result.stdout

    def checkpoint(self, container_id, checkpoint_name="uat-checkpoint"):
        if not self.is_available():
            return False, "docker not installed"
        result = subprocess.run(
            ["docker", "checkpoint", "create", container_id, checkpoint_name],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            return False, result.stderr.strip() or "docker checkpoint failed"
        return True, checkpoint_name

    def restore(self, container_id, checkpoint_name="uat-checkpoint"):
        if not self.is_available():
            return False, "docker not installed"
        result = subprocess.run(
            ["docker", "start", "--checkpoint", checkpoint_name, container_id],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            return False, result.stderr.strip() or "docker restore failed"
        return True, result.stdout.strip()

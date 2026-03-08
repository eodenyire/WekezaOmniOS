import subprocess

class DockerAdapter:
    """
    Adapter for interacting with Docker containers.
    """

    def list_containers(self):
        result = subprocess.run(
            ["docker", "ps", "--format", "{{.ID}}"],
            capture_output=True,
            text=True
        )

        return result.stdout.strip().split("\n")

    def inspect_container(self, container_id):
        result = subprocess.run(
            ["docker", "inspect", container_id],
            capture_output=True,
            text=True
        )

        return result.stdout

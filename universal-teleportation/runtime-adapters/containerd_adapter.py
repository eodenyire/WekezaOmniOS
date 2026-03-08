import subprocess

class ContainerdAdapter:

    def is_available(self):
        result = subprocess.run(["which", "ctr"], capture_output=True, text=True)
        return result.returncode == 0

    def list_containers(self):
        if not self.is_available():
            return []
        result = subprocess.run(
            ["ctr", "containers", "list"],
            capture_output=True,
            text=True
        )

        lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
        if len(lines) <= 1:
            return []
        # Skip header row in ctr output
        return [line.split()[0] for line in lines[1:]]

    def checkpoint(self, container_id, checkpoint_name="uat-checkpoint"):
        # Containerd checkpoint flows vary by setup. Keep a safe placeholder behavior.
        if not self.is_available():
            return False, "containerd (ctr) not installed"
        return False, f"checkpoint not implemented for containerd container {container_id}"

    def restore(self, container_id, checkpoint_name="uat-checkpoint"):
        if not self.is_available():
            return False, "containerd (ctr) not installed"
        return False, f"restore not implemented for containerd container {container_id}"

import subprocess

class ContainerdAdapter:

    def list_containers(self):
        result = subprocess.run(
            ["ctr", "containers", "list"],
            capture_output=True,
            text=True
        )

        return result.stdout

import subprocess

def checkpoint_container(container_id, checkpoint_name="uat-checkpoint"):
    """
    Create container checkpoint.
    """

    cmd = [
        "docker",
        "checkpoint",
        "create",
        container_id,
        checkpoint_name,
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            return False, checkpoint_name, result.stderr.strip() or "docker checkpoint failed"
        return True, checkpoint_name, "ok"
    except FileNotFoundError:
        return False, checkpoint_name, "docker command not found"

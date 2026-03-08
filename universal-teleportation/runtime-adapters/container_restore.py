import subprocess

def restore_container(container_id, checkpoint_name):
    """
    Restore container from checkpoint.
    """

    cmd = [
        "docker",
        "start",
        "--checkpoint",
        checkpoint_name,
        container_id,
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            return False, result.stderr.strip() or "docker restore failed"
        return True, result.stdout.strip() or container_id
    except FileNotFoundError:
        return False, "docker command not found"

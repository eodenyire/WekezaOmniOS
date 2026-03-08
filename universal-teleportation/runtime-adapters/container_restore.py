import subprocess

def restore_container(container_id, checkpoint_name):
    """
    Restore container from checkpoint.
    """

    subprocess.run([
        "docker",
        "start",
        "--checkpoint",
        checkpoint_name,
        container_id
    ])

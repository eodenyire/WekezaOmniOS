import subprocess

def checkpoint_container(container_id, checkpoint_name="uat-checkpoint"):
    """
    Create container checkpoint.
    """

    subprocess.run([
        "docker",
        "checkpoint",
        "create",
        container_id,
        checkpoint_name
    ])

    return checkpoint_name

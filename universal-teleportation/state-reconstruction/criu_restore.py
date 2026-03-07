# criu_restore.py
# Wrapper around CRIU restore.
# Example:

import subprocess

def restore(directory):

    cmd = [
        "criu",
        "restore",
        "-D", directory,
        "--shell-job"
    ]

    subprocess.run(cmd)

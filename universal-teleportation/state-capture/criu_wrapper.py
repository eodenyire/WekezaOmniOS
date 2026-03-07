#Interface to CRIU commands.
# Uses subprocess.
# Example:

import subprocess

def checkpoint_process(pid, directory):

    cmd = [
        "criu",
        "dump",
        "-t", str(pid),
        "-D", directory,
        "--shell-job"
    ]

    subprocess.run(cmd)

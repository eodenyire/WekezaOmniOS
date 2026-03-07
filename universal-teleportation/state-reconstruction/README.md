4️⃣ state-reconstruction

Recreates the process.

restore_memory()
restore_threads()
restore_file_descriptors()
resume_execution()

3️⃣ state-reconstruction

Restores process.

state-reconstruction/

restore_manager.py
criu_restore.py
environment_loader.py
restore_manager.py

Main restore logic.

Example:

def restore_process(snapshot_dir):

    print("Restoring process from snapshot")
criu_restore.py

Wrapper around CRIU restore.

Example:

import subprocess

def restore(directory):

    cmd = [
        "criu",
        "restore",
        "-D", directory,
        "--shell-job"
    ]

    subprocess.run(cmd)

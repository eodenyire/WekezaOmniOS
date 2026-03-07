# snapshot_builder.py
# Creates portable snapshot.
# Example:

import tarfile

def build_snapshot(snapshot_dir, output_file):

    with tarfile.open(output_file, "w:gz") as tar:
        tar.add(snapshot_dir)

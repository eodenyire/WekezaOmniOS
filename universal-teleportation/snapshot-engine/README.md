2️⃣ snapshot-engine

Packages process state.

process_snapshot.bin
memory_pages.bin
environment.json
dependencies.json

This becomes a portable execution snapshot.

2️⃣ snapshot-engine

Packages captured state.

snapshot-engine/

snapshot_builder.py
snapshot_reader.py
snapshot_metadata.py
snapshot_builder.py

Creates portable snapshot.

Example:

import tarfile

def build_snapshot(snapshot_dir, output_file):

    with tarfile.open(output_file, "w:gz") as tar:
        tar.add(snapshot_dir)

Output:

snapshots/process_1821_snapshot.tar.gz
snapshot_metadata.py

Stores metadata.

Example:

{
  "process_id": 1821,
  "timestamp": "2026-03-07T18:20:00",
  "os": "ubuntu",
  "memory_size": "120MB"
}

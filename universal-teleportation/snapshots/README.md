# snapshots

## Purpose
Stores generated snapshot archives, checkpoint directories, and inbound transferred snapshots for teleportation operations.

## Current Structure
- Checkpoint and process directories (for example `phase3-checkpoint`, `process_*`).
- `remote-inbox/`: Received snapshots pending processing.
- Compressed snapshot artifacts (`*.tar.gz`) for demos/tests.

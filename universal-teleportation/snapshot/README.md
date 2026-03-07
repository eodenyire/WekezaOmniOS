Rule 6 — Snapshots Must Be Portable

Snapshots must not depend on a machine.

So snapshot structure must be universal.

snapshot/

metadata.json
memory.dump
filesystem.tar
env.json

Example metadata:

{
 "process_id": 1821,
 "os": "ubuntu",
 "architecture": "x86_64",
 "created_at": "2026-03-07T18:20:00"
}

Portability enables future teleportation across nodes.

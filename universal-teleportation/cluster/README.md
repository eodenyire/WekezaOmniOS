# WekezaOmniOS Cluster Module

The `cluster` module manages teleportation nodes for the Universal Application Teleportation (UAT) engine.

## Responsibilities

- Node registry
- Node health monitoring
- Future distributed teleportation support
- Integration with CLI and API

---

## Architecture
+----------------+
| CLI / API |
+----------------+
|
v
+----------------+
| Cluster Module |
+----------------+
|
v
+---------------------------+
| Nodes (local / remote) |
+---------------------------+



Currently Phase 1 uses **local node simulation**.

---

## Folder Structure
cluster/
README.md
node_registry.py
node_health_monitor.py
utils.py



---

## Integration

- CLI `teleport` commands can query `cluster` for node information
- API endpoints can later call `cluster` to dispatch teleportation requests across nodes
- `state-capture` and `snapshot-engine` will call cluster to determine **where to restore a process**

Perfect. You’re now moving to the **`cluster/` folder**, which is part of Phase 1’s preparation for **future distributed teleportation**, even though Phase 1 is still local.

We’ll **design it the same way we did for `api/` and `cli/`**: full documentation, architecture, integration notes, and placeholders for the first Python files.

---

# 📁 Folder: `cluster/`

Purpose:
Manage nodes in the teleportation environment. Even in Phase 1, we simulate **a multi-node architecture** for the engine. This prepares the system for **Phase 2**, where teleportation happens across machines.

Responsibilities:

* Maintain **registry of nodes** (even if only local for now)
* Track **node health**
* Provide **future API endpoints** for distributed teleportation
* Provide **integration points** for CLI and API

---

# 📄 `README.md`

```md
# WekezaOmniOS Cluster Module

The `cluster` module manages teleportation nodes for the Universal Application Teleportation (UAT) engine.

## Responsibilities

- Node registry
- Node health monitoring
- Future distributed teleportation support
- Integration with CLI and API

---

## Architecture

```

+----------------+
| CLI / API      |
+----------------+
|
v
+----------------+
| Cluster Module |
+----------------+
|
v
+---------------------------+
| Nodes (local / remote)    |
+---------------------------+

```

Currently Phase 1 uses **local node simulation**.

---

## Folder Structure

```

cluster/
README.md
node_registry.py
node_health_monitor.py
utils.py

```

---

## Integration

- CLI `teleport` commands can query `cluster` for node information
- API endpoints can later call `cluster` to dispatch teleportation requests across nodes
- `state-capture` and `snapshot-engine` will call cluster to determine **where to restore a process**
```

---

# 📄 `node_registry.py`

Purpose: Maintain a registry of nodes (currently only local nodes).

```python
class NodeRegistry:
    def __init__(self):
        # Nodes will be stored as {node_name: info_dict}
        self.nodes = {}

    def add_node(self, name, info):
        self.nodes[name] = info
        print(f"[Cluster] Node '{name}' added.")

    def remove_node(self, name):
        if name in self.nodes:
            del self.nodes[name]
            print(f"[Cluster] Node '{name}' removed.")

    def list_nodes(self):
        return self.nodes
```

Example usage:

```python
registry = NodeRegistry()
registry.add_node("local-node", {"ip": "127.0.0.1", "status": "active"})
print(registry.list_nodes())
```

---

# 📄 `node_health_monitor.py`

Purpose: Check node status. For Phase 1, this **simulates local health checks**.

```python
import time

class NodeHealthMonitor:
    def __init__(self, registry):
        self.registry = registry

    def check_nodes(self):
        for node, info in self.registry.list_nodes().items():
            # For now, simulate all nodes as active
            info["status"] = "active"
            print(f"[Cluster] Node '{node}' is {info['status']}")
```

---

# 📄 `utils.py`

Helper functions for cluster module.

```python
def validate_node_name(name):
    if not name:
        raise ValueError("Node name cannot be empty")
    return name

def generate_node_id(name):
    return f"node_{name.lower()}"
```

---

# 🔗 Integration Plan

Even in Phase 1:

```text
CLI → Cluster Module → Node Registry / Health Monitor → Snapshot Engine
```

* `teleport restore` could check **available nodes** from `cluster/node_registry.py`
* `state-capture` could later register **node metadata**
* Sets stage for **Phase 2: multi-node teleportation**

---

# 📂 Final `cluster/` Folder Structure

```text
cluster/
    README.md
    node_registry.py
    node_health_monitor.py
    utils.py
```

---

✅ **Next Step:**

We continue Phase 1 by moving into the **`configs/` folder**, which is critical to define **system-wide settings** for teleportation, CRIU paths, snapshot directories, and logging.

Do you want me to design `configs/` next?

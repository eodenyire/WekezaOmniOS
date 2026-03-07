# 🏗️ WekezaOmniOS: Cluster Module

The **Cluster Module** is the orchestration layer responsible for managing teleportation nodes. It maintains the global state of where a process can be moved and ensures that target environments are healthy before a "jump" is initiated.

### 🎯 Purpose

* **Node Registry:** A centralized directory of all available teleportation nodes (local, remote, or cloud).
* **Health Telemetry:** Real-time monitoring of node availability and resource stress.
* **Orchestration Bridge:** Acts as the middleman between the CLI/API and the physical hardware.

---

## 🛠️ Module Breakdown

| File | Responsibility |
| --- | --- |
| **`node_registry.py`** | Manages the addition, removal, and listing of teleportation nodes. |
| **`node_health_monitor.py`** | Simulates health checks to ensure target nodes are ready for restoration. |
| **`utils.py`** | Helper functions for node validation and unique ID generation. |

---

## 🔄 Integration Workflow

In **Phase 1**, the cluster module simulates a multi-node environment on your local machine to test the registry logic:

1. **Registry:** `node_registry.py` initializes with a "localhost" entry.
2. **Validation:** Before a `capture` command finishes, the CLI checks the registry for a valid destination node.
3. **Handoff:** The `snapshot-engine` uses cluster metadata to tag the snapshot for the correct target architecture.

---

### 📄 `node_registry.py`

```python
"""
WekezaOmniOS Node Registry
Maintains the inventory of valid teleportation targets.
"""

class NodeRegistry:
    def __init__(self):
        # Nodes stored as {node_id: metadata_dict}
        self.nodes = {}

    def add_node(self, name, ip="127.0.0.1", status="active"):
        node_id = f"node_{name.lower().replace(' ', '_')}"
        self.nodes[node_id] = {
            "name": name,
            "ip": ip,
            "status": status,
            "architecture": "x86_64"  # Default for Phase 1
        }
        print(f"[Cluster] Node '{name}' registered successfully with ID: {node_id}")

    def remove_node(self, node_id):
        if node_id in self.nodes:
            del self.nodes[node_id]
            print(f"[Cluster] Node ID '{node_id}' removed from registry.")

    def list_nodes(self):
        """Returns the current fleet of nodes."""
        return self.nodes

```

---

### 📄 `node_health_monitor.py`

```python
"""
WekezaOmniOS Node Health Monitor
Simulates heartbeats and resource checks for cluster nodes.
"""

import time

class NodeHealthMonitor:
    def __init__(self, registry):
        self.registry = registry

    def perform_heartbeat(self):
        """Simulates a health check across the registry."""
        print("\n[Cluster] Initiating node health sweep...")
        for node_id, info in self.registry.list_nodes().items():
            # Phase 1 Mock: All local nodes are assumed healthy
            info["last_heartbeat"] = time.time()
            info["status"] = "active"
            print(f" -> Node: {info['name']} | Status: {info['status']} | Latency: 0.1ms")

```

---

### 📄 `utils.py`

```python
"""
WekezaOmniOS Cluster Utilities
"""

def validate_node_name(name):
    """Ensures node names are URL and filesystem friendly."""
    if not name or len(name) < 3:
        raise ValueError("Node name must be at least 3 characters long.")
    return name.strip().lower().replace(" ", "-")

def generate_node_id(name):
    """Generates a standardized ID for the registry."""
    clean_name = validate_node_name(name)
    return f"node_{clean_name}"

```

---

### ✅ Module Integration Status

With these files, **WekezaOmniOS** now has a "Memory" of its environment. You've moved from a script that just runs commands to a **system** that understands its own infrastructure.

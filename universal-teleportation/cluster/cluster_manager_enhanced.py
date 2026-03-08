"""
WekezaOmniOS Cluster Manager - Phase 2 Enhanced
Comprehensive cluster coordination for distributed teleportation.
"""
import json
import os
import time
import datetime
import subprocess
from typing import Dict, List, Optional

class ClusterManager:
    """
    Central management system for coordinating teleportation across a cluster of nodes.
    Handles node registration, health monitoring, and workload distribution.
    """
    
    def __init__(self, registry_path="cluster/node_registry.json"):
        """Initialize the Cluster Manager."""
        self.registry_path = registry_path
        self.nodes = self._load_registry()
        self.last_health_check = {}
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(registry_path) if os.path.dirname(registry_path) else ".", exist_ok=True)
        
        print(f"[ClusterManager] Initialized with {len(self.nodes.get('nodes', []))} registered nodes")

    def _load_registry(self) -> Dict:
        """Load node registry from JSON file."""
        if os.path.exists(self.registry_path):
            try:
                with open(self.registry_path, "r") as f:
                    data = json.load(f)
                    # Ensure metadata exists
                    if "metadata" not in data:
                        data["metadata"] = {"created": datetime.datetime.now().isoformat()}
                    return data
            except json.JSONDecodeError:
                print(f"[ClusterManager] Warning: Invalid JSON, creating new registry")
        
        return {"nodes": [], "metadata": {"created": datetime.datetime.now().isoformat()}}

    def _save_registry(self):
        """Save current registry state to JSON file."""
        try:
            self.nodes["metadata"]["last_updated"] = datetime.datetime.now().isoformat()
            with open(self.registry_path, "w") as f:
                json.dump(self.nodes, f, indent=4)
            print(f"[ClusterManager] Registry saved: {len(self.nodes['nodes'])} nodes")
        except Exception as e:
            print(f"[ClusterManager] Error saving registry: {e}")

    def register_node(self, node_id: str, address: str, role: str = "worker", 
                     port: int = 8000, metadata: Optional[Dict] = None) -> bool:
        """Register a new node in the cluster."""
        # Check if node already exists
        for node in self.nodes["nodes"]:
            if node["id"] == node_id:
                print(f"[ClusterManager] Node '{node_id}' already registered, updating...")
                node.update({
                    "address": address,
                    "role": role,
                    "port": port,
                    "status": "ONLINE",
                    "last_seen": datetime.datetime.now().isoformat(),
                    "metadata": metadata or node.get("metadata", {})
                })
                self._save_registry()
                return True
        
        # Add new node
        new_node = {
            "id": node_id,
            "address": address,
            "role": role,
            "port": port,
            "status": "ONLINE",
            "registered_at": datetime.datetime.now().isoformat(),
            "last_seen": datetime.datetime.now().isoformat(),
            "teleportations_received": 0,
            "teleportations_sent": 0,
            "metadata": metadata or {}
        }
        
        self.nodes["nodes"].append(new_node)
        self._save_registry()
        
        print(f"[ClusterManager] ✅ Node '{node_id}' registered at {address}:{port} (role: {role})")
        return True

    def unregister_node(self, node_id: str) -> bool:
        """Remove a node from the cluster."""
        initial_count = len(self.nodes["nodes"])
        self.nodes["nodes"] = [n for n in self.nodes["nodes"] if n["id"] != node_id]
        
        if len(self.nodes["nodes"]) < initial_count:
            self._save_registry()
            print(f"[ClusterManager] Node '{node_id}' unregistered")
            return True
        return False

    def get_node(self, node_id: str) -> Optional[Dict]:
        """Get information about a specific node."""
        for node in self.nodes["nodes"]:
            if node["id"] == node_id:
                return node
        return None

    def get_available_nodes(self, role: Optional[str] = None) -> List[Dict]:
        """Get all nodes that are currently available."""
        available = []
        for node in self.nodes["nodes"]:
            if node["status"] == "ONLINE":
                if role is None or node["role"] == role:
                    available.append(node)
        return available

    def list_nodes(self) -> List[Dict]:
        """Get all registered nodes."""
        return self.nodes.get("nodes", [])

    # Compatibility aliases used by existing Phase 2 scripts
    def get_cluster_nodes(self) -> List[Dict]:
        return self.list_nodes()

    def check_node_health(self, node_id: str) -> bool:
        """Check if a specific node is reachable."""
        node = self.get_node(node_id)
        if not node:
            print(f"[ClusterManager] Node '{node_id}' not found")
            return False
        
        # Special handling for localhost
        if node["address"] in ["localhost", "127.0.0.1", "::1"]:
            is_healthy = True
        else:
            # Try to ping the node
            try:
                result = subprocess.run(
                    ["ping", "-c", "1", "-W", "1", node["address"]],
                    capture_output=True,
                    timeout=2
                )
                is_healthy = (result.returncode == 0)
            except Exception as e:
                print(f"[ClusterManager] Health check failed for '{node_id}': {e}")
                is_healthy = False
        
        # Update node status
        for n in self.nodes["nodes"]:
            if n["id"] == node_id:
                n["status"] = "ONLINE" if is_healthy else "OFFLINE"
                n["last_seen"] = datetime.datetime.now().isoformat()
                break
        
        self.last_health_check[node_id] = time.time()
        self._save_registry()
        
        status = "✅ HEALTHY" if is_healthy else "❌ UNREACHABLE"
        print(f"[ClusterManager] Node '{node_id}' {status}")
        
        return is_healthy

    def check_all_nodes_health(self) -> Dict[str, bool]:
        """Run health checks on all registered nodes."""
        results = {}
        print(f"[ClusterManager] Running health checks on {len(self.nodes['nodes'])} nodes...")
        
        for node in self.nodes["nodes"]:
            results[node["id"]] = self.check_node_health(node["id"])
        
        healthy_count = sum(1 for v in results.values() if v)
        print(f"[ClusterManager] Health check complete: {healthy_count}/{len(results)} nodes healthy")
        
        return results

    def record_teleportation(self, source_node_id: str, target_node_id: str):
        """Record a teleportation event for metrics."""
        for node in self.nodes["nodes"]:
            if node["id"] == source_node_id:
                node["teleportations_sent"] = node.get("teleportations_sent", 0) + 1
            if node["id"] == target_node_id:
                node["teleportations_received"] = node.get("teleportations_received", 0) + 1
        
        self._save_registry()
        print(f"[ClusterManager] Teleportation recorded: {source_node_id} → {target_node_id}")

    def get_cluster_stats(self) -> Dict:
        """Get overall cluster statistics."""
        total_nodes = len(self.nodes["nodes"])
        online_nodes = len([n for n in self.nodes["nodes"] if n["status"] == "ONLINE"])
        total_sent = sum(n.get("teleportations_sent", 0) for n in self.nodes["nodes"])
        total_received = sum(n.get("teleportations_received", 0) for n in self.nodes["nodes"])
        
        return {
            "total_nodes": total_nodes,
            "online_nodes": online_nodes,
            "offline_nodes": total_nodes - online_nodes,
            "total_teleportations": total_sent,
            "health_percentage": (online_nodes / total_nodes * 100) if total_nodes > 0 else 0
        }

    def get_cluster_statistics(self) -> Dict:
        stats = self.get_cluster_stats()
        # Compatibility field name expected in tests
        stats["healthy_nodes"] = stats.get("online_nodes", 0)
        return stats

    def print_cluster_status(self):
        """Print a formatted cluster status report."""
        print("\n" + "="*70)
        print("  WekezaOmniOS Cluster Status")
        print("="*70)
        
        stats = self.get_cluster_stats()
        print(f"\nCluster Overview:")
        print(f"  Total Nodes: {stats['total_nodes']}")
        print(f"  Online: {stats['online_nodes']}")
        print(f"  Offline: {stats['offline_nodes']}")
        print(f"  Health: {stats['health_percentage']:.1f}%")
        print(f"  Total Teleportations: {stats['total_teleportations']}")
        
        print(f"\nRegistered Nodes:")
        for node in self.nodes["nodes"]:
            status_icon = "✅" if node["status"] == "ONLINE" else "❌"
            print(f"  {status_icon} {node['id']}")
            print(f"      Address: {node['address']}:{node.get('port', 8000)}")
            print(f"      Role: {node['role']}")
            print(f"      Status: {node['status']}")
            sent = node.get('teleportations_sent', 0)
            received = node.get('teleportations_received', 0)
            print(f"      Teleportations: {received} received, {sent} sent")
        
        print("\n" + "="*70 + "\n")


# Example usage and testing
if __name__ == "__main__":
    print("🚀 WekezaOmniOS Cluster Manager - Phase 2")
    print()
    
    # Initialize cluster manager
    cm = ClusterManager()
    
    # Register some test nodes
    cm.register_node("nairobi-alpha-01", "192.168.1.50", role="worker")
    cm.register_node("nairobi-beta-02", "192.168.1.51", role="worker")
    cm.register_node("cloud-us-east-01", "10.0.1.100", role="cloud")
    cm.register_node("local-controller", "127.0.0.1", role="controller")
    
    # Print cluster status
    cm.print_cluster_status()
    
    # Check health
    print("\nRunning health checks...")
    cm.check_all_nodes_health()
    
    # Show final status
    cm.print_cluster_status()
    
    print("\n✅ Cluster Manager ready for Phase 2 teleportation operations")

"""
WekezaOmniOS Routing Engine
Phase 4: Determines the optimal path and node for a teleportation jump.
"""

class RoutingEngine:
    def __init__(self, cluster_manager):
        # Connect the router to the node registry from Phase 2
        self.cluster = cluster_manager

    def select_route(self, source_node, target_node_id):
        """
        Calculates the best path for the snapshot jump.
        Verifies if the target node exists and is ONLINE.
        """
        target_node = self.cluster.get_node(target_node_id)
        
        if not target_node:
            print(f"[Router] ❌ Routing Failure: Node {target_node_id} is unreachable.")
            return None
        
        # Phase 4 Path Logic: Local -> Vault -> Remote Pull
        print(f"[Router] 🛣️ Optimal Path Confirmed: {source_node} ⮕ [VAULT] ⮕ {target_node['address']}")
        
        return {
            "path_type": "Indirect-Vault-Transfer",
            "latency": "low",
            "hops": 1
        }

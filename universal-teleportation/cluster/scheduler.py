"""Simple scheduling policy for Phase 2 target selection."""


class Scheduler:
    """Picks a target node with a deterministic score-based policy."""

    def choose_target(self, nodes, preferred_role=None):
        """
        Args:
            nodes: list[dict] or dict[str, dict]
            preferred_role: optional role preference (e.g. 'worker', 'cloud')
        """
        if isinstance(nodes, dict):
            node_list = [{"id": k, **v} for k, v in nodes.items()]
        else:
            node_list = list(nodes)

        online_nodes = [n for n in node_list if n.get("status", "ONLINE") == "ONLINE"]
        if preferred_role:
            role_filtered = [n for n in online_nodes if n.get("role") == preferred_role]
            if role_filtered:
                online_nodes = role_filtered

        if not online_nodes:
            return None

        # Lower load wins; if absent assume medium load.
        def score(node):
            return (
                float(node.get("metadata", {}).get("load", 0.5)),
                -int(node.get("metadata", {}).get("memory_free_mb", 0)),
                node.get("id", ""),
            )

        return sorted(online_nodes, key=score)[0]


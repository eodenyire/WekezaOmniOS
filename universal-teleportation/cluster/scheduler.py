class Scheduler:
    """
    Decides where a teleported workload should go.
    Returns the first available node, or None if no nodes are registered.
    """

    def choose_target(self, nodes):
        for node_id, node in nodes.items():
            return node
        return None

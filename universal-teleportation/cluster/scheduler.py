class Scheduler:
    """
    Decides where a teleported workload should go.
    """

    def choose_target(self, nodes):
        for node_id, node in nodes.items():
            return node

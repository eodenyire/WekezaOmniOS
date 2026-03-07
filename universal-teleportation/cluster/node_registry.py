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

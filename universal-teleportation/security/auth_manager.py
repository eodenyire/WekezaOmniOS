class AuthManager:
    """
    Validates node authentication.
    """

    def __init__(self):
        self.trusted_nodes = {}

    def register_node(self, node_id, certificate):

        self.trusted_nodes[node_id] = certificate

    def authenticate(self, node_id, certificate):

        trusted = self.trusted_nodes.get(node_id)

        return trusted == certificate

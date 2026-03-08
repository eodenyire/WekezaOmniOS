import uuid

class NodeIdentity:

    def __init__(self, node_name):

        self.node_name = node_name
        self.node_id = str(uuid.uuid4())

    def get_identity(self):

        return {
            "node_name": self.node_name,
            "node_id": self.node_id
        }

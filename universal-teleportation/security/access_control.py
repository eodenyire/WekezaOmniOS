class AccessControl:

    def __init__(self):

        self.permissions = {}

    def allow(self, node_id, action):

        self.permissions.setdefault(node_id, []).append(action)

    def check(self, node_id, action):

        return action in self.permissions.get(node_id, [])

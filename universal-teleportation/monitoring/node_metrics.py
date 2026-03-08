class NodeMetrics:

    def __init__(self):
        self.teleportations = 0

    def record_teleport(self):
        self.teleportations += 1

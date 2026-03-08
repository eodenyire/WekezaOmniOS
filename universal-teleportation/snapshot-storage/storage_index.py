class StorageIndex:

    def __init__(self):
        self.index = {}

    def register_snapshot(self, snapshot_id, location):

        self.index[snapshot_id] = location

    def get_snapshot(self, snapshot_id):

        return self.index.get(snapshot_id)

    def list_snapshots(self):

        return list(self.index.keys())

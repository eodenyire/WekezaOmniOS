import os
import shutil

class LocalStorage:

    def __init__(self, storage_dir="snapshot-storage/data"):
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)

    def save(self, snapshot_path, snapshot_id):

        destination = os.path.join(self.storage_dir, snapshot_id)

        shutil.copytree(snapshot_path, destination)

        return destination

    def load(self, snapshot_id):

        return os.path.join(self.storage_dir, snapshot_id)

    def list(self):

        return os.listdir(self.storage_dir)

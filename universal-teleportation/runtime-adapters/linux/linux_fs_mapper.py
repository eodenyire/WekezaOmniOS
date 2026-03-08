class LinuxFSMapper:

    def map_path(self, path):

        return path.replace("C:\\", "/mnt/c/")

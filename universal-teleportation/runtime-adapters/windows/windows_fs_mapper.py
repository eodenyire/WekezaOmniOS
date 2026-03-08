class WindowsFSMapper:

    def map_path(self, path):

        return path.replace("/home/", "C:\\Users\\")

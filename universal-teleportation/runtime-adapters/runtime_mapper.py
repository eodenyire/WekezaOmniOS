class RuntimeMapper:
    """
    Selects the appropriate runtime adapter.
    """

    def __init__(self):

        self.adapters = {}

    def register_adapter(self, os_name, adapter):

        self.adapters[os_name] = adapter

    def get_adapter(self, os_name):

        return self.adapters.get(os_name)

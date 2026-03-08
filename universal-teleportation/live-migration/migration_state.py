class MigrationState:

    def __init__(self):

        self.state = "INITIAL"

    def update(self, new_state):

        self.state = new_state

    def get_state(self):

        return self.state

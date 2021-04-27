from Utilities.StartManagers.StartManager import StartManager


class PingStartManager(StartManager):

    def __init__(self, run_mode):
        super().__init__(run_mode)

    def start(self):
        pass

    def run_in_interactive(self):
        pass

    def run_in_non_interactive(self):
        pass

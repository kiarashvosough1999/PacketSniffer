from DataModels.Enums.RunMode import RunMode


class StartManager:

    def __init__(self,run_mode):
        self.run_mode = run_mode

    def start(self):
        if self.run_mode == RunMode.interactive:
            self.run_in_interactive()
        else:
            self.run_in_non_interactive()

    def run_in_interactive(self):
        pass

    def run_in_non_interactive(self):
        pass

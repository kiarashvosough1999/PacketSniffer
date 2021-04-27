import sys
from DataModels.Enums.AppMode import AppMode
from DataModels.Enums.RunMode import RunMode
from Utilities.StartManagers.PingStartManager import PingStartManager
from Utilities.StartManagers.PortScannerStartManager import PortScannerStartManager
from Utilities.StartManagers.StartManager import StartManager
from Utilities.Threading.ThreadingUtilities import ThreadingUtilities
from Utilities.ValidationManager import ValidationManager
import argparse


class AppStartManager(StartManager):

    def __init__(self, run_mode):
        super().__init__(run_mode)
        self.max_thread = 0

    def start(self):
        self.max_thread = ThreadingUtilities.start_new_process_to_get_max_threads()
        if self.max_thread <= 0:
            print('There is not enough resourses to run the program,'
                  ' try to free more ram and try again')
        print('You can run {} threads concurently,'
              ' do not try to hit the limit unless there is no guarantee to work '
              'properly'.format(self.max_thread))
        if len(sys.argv) > 1:
            self.run_mode = RunMode.non_interactive
        else:
            self.run_mode = RunMode.interactive

        self.detect_app_mode()

    def detect_app_mode(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('AppMode',
                            metavar='appmode',
                            type=str,
                            help='you should at least choose your app mode')
        parsed = parser.parse_args()
        app_mode = ValidationManager.validate_app_mode(parsed.AppMode)
        if app_mode == AppMode.port_scanner:
            PortScannerStartManager(self.run_mode).start()
        elif app_mode == AppMode.ping:
            PingStartManager(self.run_mode).start()

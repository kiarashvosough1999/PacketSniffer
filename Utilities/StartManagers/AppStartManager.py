import sys
from DataModels.Enums.AppMode import AppMode
from DataModels.Enums.RunMode import RunMode
from Utilities.StartManagers.ARPStartManager import ARPStartManager
from Utilities.StartManagers.HOPStartManager import HOPStartManager
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

    def check_for_max_thread(self):
        self.max_thread = ThreadingUtilities.start_new_process_to_get_max_threads()
        if self.max_thread <= 0:
            print('There is not enough resourses to run the program,'
                  ' try to free more ram and try again')
        print('You can run {} threads concurently,'
              ' do not try to hit the limit unless there is no guarantee to work '
              'properly'.format(self.max_thread))

    def start(self):
        if len(sys.argv) > 1:
            self.run_mode = RunMode.non_interactive
        else:
            self.run_mode = RunMode.interactive

        self.detect_app_mode()

    def detect_app_mode(self):
        # parser = argparse.ArgumentParser()
        # parser.add_argument('AppMode',
        #                     metavar='appmode',
        #                     type=str,
        #                     help='you should at least choose your app mode')
        # parsed = parser.parse_args()
        global app_mode
        if len(sys.argv) >= 2:
            app_mode = sys.argv[1]
        else:
            print('you should at least choose your app mode')
            exit(0)
        app_mode = ValidationManager.validate_app_mode(app_mode)
        if app_mode == AppMode.port_scanner:
            self.check_for_max_thread()
            PortScannerStartManager(self.run_mode,self.max_thread).start()
        elif app_mode == AppMode.ping:
            self.check_for_max_thread()
            st = PingStartManager(self.run_mode)
            st.max_thread = self.max_thread
            st.start()
        elif app_mode == AppMode.hop:
            st = HOPStartManager(self.run_mode)
            st.start()
        elif app_mode == AppMode.arp:
            arp = ARPStartManager(run_mode=self.run_mode)
            arp.start()

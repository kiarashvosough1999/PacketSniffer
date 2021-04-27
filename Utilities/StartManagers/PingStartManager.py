import argparse
import sys

from DataModels.PingInputsModel import PingInputsModel
from Ping.Ping import ping
from Utilities.MyExceptions import MyException
from Utilities.StartManagers.StartManager import StartManager
from Utilities.UseFullFunction import safe_cast
from Utilities.ValidationManager import ValidationManager


class PingStartManager(StartManager):

    def __init__(self, run_mode):
        super().__init__(run_mode)
        self.max_thread = 0

    def run_in_interactive(self):
        pass

    def run_in_non_interactive(self):
        try:
            my_parser = argparse.ArgumentParser(description='Ping')

            my_parser.add_argument('AppMode',
                                   metavar='appmode',
                                   type=str,
                                   help='enter your App mode')

            my_parser.add_argument('-adr',
                                   '--adresses',
                                   required=True,
                                   action='store',
                                   nargs='+',
                                   type=str,
                                   help='enter your App mode')

            my_parser.add_argument('-wt',
                                   '--waittime',
                                   type=int,
                                   help='waiting time on each port',
                                   default=1000)

            my_parser.add_argument('-ps',
                                   '--packetsize',
                                   type=int,
                                   help='size of the packet which will be sent',
                                   default=58)

            args = my_parser.parse_args()
            try:
                addreeses, wait_time, packet_size = ValidationManager.validate_ping_userInputs(self.max_thread,
                                                                                               list(args.adresses),
                                                                                              args.waittime,
                                                                                              args.packetsize)
                input_model = PingInputsModel(addreeses, args.waittime, args.packetsize)
                ping(input_model).start()
            except MyException as error:
                print(error.message)
                error.do_action2()

        except KeyboardInterrupt:
            print('exited from program with keyboard interrupt')
            sys.exit(0)

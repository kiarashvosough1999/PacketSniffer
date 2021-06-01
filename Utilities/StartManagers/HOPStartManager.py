import argparse
import sys

from TraceRoute.TraceRouter import TraceRouter
from Utilities.Exception.MyExceptions import MyException
from Utilities.StartManagers.StartManager import StartManager
from Utilities.ValidationManager import ValidationManager


class HOPStartManager(StartManager):

    def __init__(self, run_mode):
        super().__init__(run_mode)

    def run_in_interactive(self):
        pass

    def run_in_non_interactive(self):
        try:
            my_parser = argparse.ArgumentParser(description='HOP')

            my_parser.add_argument('AppMode',
                                   metavar='appmode',
                                   type=str,
                                   help='enter your App mode')

            my_parser.add_argument('-adr',
                                   '--adresse',
                                   required=True,
                                   action='store',
                                   type=str,
                                   help='enter your address')

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

            my_parser.add_argument('-mt',
                                   '--maxTTL',
                                   type=int,
                                   help='maximum ttl',
                                   default=20)

            my_parser.add_argument('-stt',
                                   '--startTTL',
                                   type=int,
                                   help='start ttl',
                                   default=0)

            my_parser.add_argument('-ht',
                                   '--hopTries',
                                   type=int,
                                   help='maximum hop tries',
                                   default=3)

            my_parser.add_argument('-st',
                                   '--startPort',
                                   type=int,
                                   help='start port',
                                   default=1)

            args = my_parser.parse_args()
            try:
                model = ValidationManager.validate_hop_info(max_ttl=args.maxTTL,
                                                            hop_tries=args.hopTries,
                                                            packet_size=args.packetsize,
                                                            waiting_time=args.waittime,
                                                            address=args.adresse,
                                                            start_port=args.startPort,
                                                            start_ttl=args.startTTL)
                TraceRouter(hop_user_inputs_model=model).start_hop()
            except MyException as error:
                print(error.message)
                error.do_action2()

        except KeyboardInterrupt:
            print('exited from program with keyboard interrupt')
            sys.exit(0)
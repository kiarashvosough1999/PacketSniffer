import argparse
import asyncio
from ARP.ARP import Arp
from Utilities.SocketManager import socketManager
from Utilities.StartManagers.StartManager import StartManager
from Utilities.ValidationManager import ValidationManager


class ARPStartManager(StartManager):

    def __init__(self, run_mode):
        super().__init__(run_mode)

    def run_in_interactive(self):
        self.run_in_non_interactive()

    def run_in_non_interactive(self):
        global connection, event_loop
        try:
            my_parser = argparse.ArgumentParser(description='Ping')

            my_parser.add_argument('AppMode',
                                   metavar='appmode',
                                   type=str,
                                   help='enter your App mode')

            my_parser.add_argument('-sip',
                                   '--startip',
                                   type=str,
                                   help='enter your start ip or mask')

            my_parser.add_argument('-eip',
                                   '--endip',
                                   type=str,
                                   help='end ip')

            my_parser.add_argument('-wt',
                                   '--waitingtime',
                                   type=int,
                                   help='waiting time',
                                   default=1000)

            args = my_parser.parse_args()

            interface, request_model = ValidationManager.validate_arp_user_inputs(start_ip=args.startip,
                                                                                  end_ip=args.endip,
                                                                                  waiting_time=args.waitingtime)

            event_loop = asyncio.get_event_loop()
            socket = socketManager.get_packet_socket(interface=interface)

            connection_trasnport = event_loop._create_connection_transport(
                socket, Arp, None, None
            )

            connection, target = event_loop.run_until_complete(connection_trasnport)
            target.send_arp_request(request_model)
            event_loop.run_forever()
        except KeyboardInterrupt:
            print("keyboard interrupt")
        finally:
            print("closing event loop")
            connection.close()
            event_loop.close()

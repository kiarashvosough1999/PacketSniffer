import socket
import sys
from DataModels.PortScanningModel import PortScanningModel
from Utilities.MyExceptions import MyException
from Utilities.Threading.ThreadingUtilities import ThreadingUtilities
from Utilities.ValidationManager import ValidationManager
from portSniffer import portSniffer
import argparse


class AppStartManager:

    def __init__(self):
        self.sys_argv = sys.argv
        self.port_data_model = None
        self.max_thread = 0

    def start(self):
        self.max_thread = ThreadingUtilities.start_new_process_to_get_max_threads()
        if self.max_thread <= 0:
            print('There is not enough resourses to run the program,'
                  ' try to free more ram and try again')
        print('You can run {} threads concurently,'
              ' do not try to hit the limit unless there is no guarantee to work '
              'properly'.format(self.max_thread))
        if len(self.sys_argv) > 1:
            self.run_on_terminal()
        else:
            self.run_in_()

    def run_on_terminal(self):
        try:
            my_parser = argparse.ArgumentParser(description='Port Sniffer')

            my_parser.add_argument('Address',
                                   metavar='address',
                                   type=str,
                                   help='your server address')
            my_parser.add_argument('Mode',
                                   metavar='mode',
                                   type=str,
                                   help='your sniifing mode')
            my_parser.add_argument('-wt',
                                   '--waittime',
                                   type=str,
                                   help='waiting time on each port',
                                   default='2')
            my_parser.add_argument('-tc',
                                   '--threadcount',
                                   type=str,
                                   help='number of threads that work',
                                   default='10')
            my_parser.add_argument('-ip',
                                   '--ipver',
                                   type=str,
                                   help='ip version',
                                   default='4')
            my_parser.add_argument('-sp',
                                   '--startport',
                                   type=str,
                                   help='start port interval',
                                   default='')
            my_parser.add_argument('-ep',
                                   '--endport',
                                   type=str,
                                   help='end port interval', default= '')

            args = my_parser.parse_args()
            try:
                mAddress, \
                mSniffing_mode, \
                mThread_num, \
                mWaiting_time, \
                custom_range, \
                mIP_version = ValidationManager.validate_userInput(address=args.Address,
                                                                   thread_num=args.threadcount,
                                                                   waiting_time=args.waittime,
                                                                   start=args.startport,
                                                                   end=args.endport,
                                                                   sniffing_mode=args.Mode,
                                                                   ip_version=args.ipver,
                                                                   max_thread=self.max_thread)
                self.port_data_model = PortScanningModel(mAddress,
                                                         mThread_num,
                                                         custom_range,
                                                         mWaiting_time,
                                                         mSniffing_mode,
                                                         mIP_version)
            except MyException as e:
                print(e.message)
                exit(0)
            except socket.gaierror or socket.error:
                print('there is something wrong with your network connection try again later.')
                print("Hostname Could Not Be Resolved !!!!")
                print("Server not responding!")
                sys.exit(0)
        except KeyboardInterrupt:
            print('exited from program with keyboard interrupt')
            sys.exit(0)
        self.start_port_sniffing()

    def run_in_(self):
        try:
            print('enter your input ->')
            while True:
                print('Address: ')
                address = input()

                print('Thread Number: ')
                thread_num = input()

                print('Port Scanning Waiting Time: ')
                waiting_time = input()

                print('ip Address version: 4.ipV4 6.ipV6 (default is ipV4, to ignore just press enter)')
                check_ip_version = input()
                if not check_ip_version:
                    check_ip_version = '4'

                print('Choose your sniffing mode: 1.All Ports\t 2.Reserved Port\t 3.application layer services')
                sniffing_mode = input()

                print('Port Start Interval: ')
                start = input()

                print('Port End Interval: ')
                end = input()

                try:
                    mAddress, \
                    mSniffing_mode, \
                    mThread_num, \
                    mWaiting_time, \
                    custom_range, \
                    mIP_version = ValidationManager.validate_userInput(address=address,
                                                                       thread_num=thread_num,
                                                                       waiting_time=waiting_time,
                                                                       start=start,
                                                                       end=end,
                                                                       sniffing_mode=sniffing_mode,
                                                                       ip_version=check_ip_version,
                                                                       max_thread=self.max_thread)
                    self.port_data_model = PortScanningModel(mAddress,
                                                             mThread_num,
                                                             custom_range,
                                                             mWaiting_time,
                                                             mSniffing_mode,
                                                             mIP_version)
                    break
                except MyException as e:
                    print(e.message)
                    continue
                except socket.gaierror or socket.error:
                    print('there is something wrong with your network connection try again later.')
                    print("Hostname Could Not Be Resolved !!!!")
                    print("Server not responding!")
                    sys.exit(0)
        except KeyboardInterrupt:
            print('exited from program with keyboard interrupt')
            sys.exit(0)
        self.start_port_sniffing()

    def start_port_sniffing(self):
        try:
            x = portSniffer(port_data_model=self.port_data_model)
            x.start()
        except KeyboardInterrupt:
            print('\tKeyboard Interrupted')
            sys.exit(0)

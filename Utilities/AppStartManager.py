import socket
import sys
import threading
import time

from DataModels.PortScanningModel import PortScanningModel
from Utilities.MyExceptions import MyExeption
from Utilities.ValidationManager import ValidationManager
from portSniffer import portSniffer


class AppStartManager:

    def __init__(self):
        self.sys_argv = sys.argv
        self.port_data_model = None
        self.max_thread = 0

    def start(self):
        self.get_max_thread_on_machine()
        print('You can run {} threads concurently, donot try to hit the limit unless there is no guarantee to work '
              'properly')
        # if len(self.sys_argv) > 1:
        #     self.run_on_terminal()
        #     self.start_port_sniffing()
        # else:
        self.run_in_interactive()

    def get_max_thread_on_machine(self):
        threads = 0
        y = 1000000
        for i in range(y):
            try:
                x = threading.Thread(target=lambda: time.sleep(1000), daemon=True)
                threads += 1
                x.start()
            except RuntimeError:
                break
        self.max_thread = threads

    # def run_on_terminal(self):
    #     global ip_version
    #     end = '1'
    #     start = '1'
    #
    #     address = self.sys_argv[1]
    #     thread_num = self.sys_argv[2]
    #     waiting_time = self.sys_argv[3]
    #     type = self.sys_argv[4]
    #     if type == '1':
    #         start = self.sys_argv[5]
    #         end = self.sys_argv[6]
    #         if len(self.sys_argv) == 8:
    #             ip_version = AppStartManager.validate_ip_version(self.sys_argv[7])
    #         else:
    #             ip_version = socket.AF_INET
    #     else:
    #         if len(self.sys_argv) == 6:
    #             ip_version = self.sys_argv[5]
    #         else:
    #             ip_version = '4'
    #     error_message, status = self.validate_userInput(address=address,
    #                                                     thread_num=thread_num,
    #                                                     waiting_time=waiting_time,
    #                                                     start=start,
    #                                                     end=end,
    #                                                     sniffing_mode=type,
    #                                                     ip_version=ip_version)
    #     if status == 0:
    #         print(error_message)
    #         exit(status)
    #     self.start_port_sniffing()

    def run_in_interactive(self):
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

                print('Choose your sniffing mode: 1.App Ports\t 2.Reserved Port\t 3.application layer services')
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
                                                                       ip_version=check_ip_version)
                    self.port_data_model = PortScanningModel(mAddress,
                                                             mThread_num,
                                                             custom_range,
                                                             mWaiting_time,
                                                             mSniffing_mode,
                                                             mIP_version)
                    break
                except MyExeption as e:
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

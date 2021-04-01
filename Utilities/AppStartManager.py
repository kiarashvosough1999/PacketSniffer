import socket
import sys
from DataModels.PortScanningModel import PortScanningModel
from Utilities.customRange import customRange
from portSniffer import portSniffer, portSniffingTask


class AppStartManager:

    def __init__(self):
        self.sys_argv = sys.argv
        self.port_data_model = None

    def start(self):
        if len(self.sys_argv) > 1:
            self.run_on_terminal()
            self.start_port_sniffing()
        else:
            self.run_in_IDE()

    def run_on_terminal(self):
        global ip_version
        end = '1'
        start = '1'

        address = self.sys_argv[1]
        thread_num = self.sys_argv[2]
        waiting_time = self.sys_argv[3]
        type = self.sys_argv[4]
        if type == '1':
            start = self.sys_argv[5]
            end = self.sys_argv[6]
            if self.sys_argv[7]:
                ip_version = AppStartManager.validate_ip_version(self.sys_argv[7])
            else:
                ip_version = socket.AF_INET
        else:
            if self.sys_argv[7]:
                ip_version = AppStartManager.validate_ip_version(self.sys_argv[5])
            else:
                ip_version = socket.AF_INET

        error_message, status = self.validate_userInput(address=address,
                                                        thread_num=thread_num,
                                                        waiting_time=waiting_time,
                                                        start=start,
                                                        end=end,
                                                        type=type,
                                                        ip_version=ip_version)
        if status == 0:
            print(error_message)
            exit(status)
        self.start_port_sniffing()

    @staticmethod
    def validate_ip_version(ip):
        if ip == '4':
            return socket.AF_INET
        elif ip == '6':
            return socket.AF_INET6
        else:
            print('no such an ip version')
            exit(0)

    def run_in_IDE(self):
        end = '1'
        start = '1'
        print('enter your input ->')
        while True:
            print('Address: ')
            address = input()

            print('Thread Number: ')
            thread_num = input()

            print('Port Scanning Waiting Time: ')
            waiting_time = input()

            print('ip Address vesrion: 4.ipV4 6.ipV6 (default is ipV4, to ignore just press enter)')
            ip_version = input()
            if ip_version != '4' or ip_version != '6':
                ip_version = '4'

            print('Choose your sniffing mode: 1.App Ports\t 2.Reserved Port\t 3.application layer services')
            type = input()

            if type == '1':
                print('Port Start Interval: ')
                start = input()
                print('Port End Interval: ')
                end = input()

            error_message, status = self.validate_userInput(address=address,
                                                            thread_num=thread_num,
                                                            waiting_time=waiting_time,
                                                            start=start,
                                                            end=end,
                                                            type=type,
                                                            ip_version=ip_version)
            if status == 0:
                print(error_message)
                continue
            else:
                break
        self.start_port_sniffing()

    def validate_userInput(self, address, thread_num, waiting_time, start, end, type, ip_version):
        mtype = portSniffingTask.get_type(type)
        if int(thread_num) and\
                int(waiting_time) and\
                int(start) and\
                int(end) and\
                (mtype is not portSniffingTask.error):

            self.port_data_model = PortScanningModel(address=address,
                                                     thread_number=int(thread_num),
                                                     portRange=customRange(int(start), int(end)),
                                                     waitingTime=int(waiting_time),
                                                     task_type=mtype,
                                                     ip_version=AppStartManager.validate_ip_version(ip_version))
            if self.port_data_model.valid_ip_type():
                return '', 1
            else:
                return 'IP address is not valid enter your inputs again', 0
        else:
            return 'there was a mistake in input data enter your inputs again', 0

    def start_port_sniffing(self):
        try:
            x = portSniffer(port_data_model=self.port_data_model)
            x.start()
        except KeyboardInterrupt:
            print('\tKeyborad Interrupted')
            sys.exit(0)

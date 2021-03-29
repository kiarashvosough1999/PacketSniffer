import socket
from threading import Thread

from Utilities.portManager import reservedPortServices


class portSniffer:

    def __init__(self, port_data_model):
        self.port_data_model = port_data_model
        self.last_port_check_attemp = port_data_model.portRange.start
        socket.setdefaulttimeout(port_data_model.waitingTime)
        self.excuting_thread = []
        self.end = False

    def start(self):
        while True:
            count = 0
            for thread in self.excuting_thread:
                if thread.is_alive():
                    count += 1
            if count == 0 and self.end:
                exit(0)
            elif count == 0:
                self.excuting_thread.clear()
                self.execute_check_procedure()

    def execute_check_procedure(self):

        end = self.last_port_check_attemp + self.port_data_model.thread_number
        start = self.last_port_check_attemp
        if end > self.port_data_model.portRange.end:
            end = self.port_data_model.portRange.end + 1
            self.end = True

        self.last_port_check_attemp += self.port_data_model.thread_number

        for port in range(start, end):
            thread = Thread(target=self.check, args=(port,))
            thread.daemon = True
            self.excuting_thread.append(thread)
            thread.start()
            thread.join(0.01)

    def check(self, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            flag = sock.connect_ex((self.port_data_model.address, port))
            if flag == 0:
                if reservedPortServices.contains_port(port):
                    print("Port {} is open with {}".format(port,reservedPortServices.get_name([port])))
                else:
                    print("Port {} is open".format(port))
            else:
                print("Port {} is not open".format(port))
            sock.close()
        except socket.gaierror:
            print("Hostname Could Not Be Resolved !!!!")
            return
        except socket.error:
            print("Server not responding!")
            return
        except KeyboardInterrupt:
            exit(0)
        return

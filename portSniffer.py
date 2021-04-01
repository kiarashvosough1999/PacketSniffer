import socket
from threading import Thread
from Utilities.portManager import reservedPortServices
from DataModels.portModel import portModel
from Utilities.portSniffingTask import portSniffingTask


class portSniffer:

    def __init__(self, port_data_model):
        self.port_data_model = port_data_model
        self.last_port_check_attemp = port_data_model.portRange.start
        socket.setdefaulttimeout(port_data_model.waitingTime)
        self.excuting_thread = []
        self.end = False
        self.thread_queue = []
        self.task_type = port_data_model.task_type
        self.opened_port = 0

    def prompt_after_compeletion(self):
        if self.opened_port > 0:
            print('{} port were opend'.format(self.opened_port))
        else:
            print('no open ports in selcted mode found')

    def start(self):
        self.create_task()
        while self.thread_queue:
            count = 0
            for thread in self.excuting_thread:
                if thread.is_alive():
                    count += 1
            if count == 0 and self.end:
                self.prompt_after_compeletion()
                exit(0)
            elif count == 0:
                self.excuting_thread.clear()
                self.execute_check_procedure()

    def create_task(self):
        if self.task_type == portSniffingTask.all_port:
            for port in range(0, 65535):
                self.thread_queue.append(portModel('', port, '', True, False))

        elif self.task_type == portSniffingTask.reserved_port:
            for port in range(self.port_data_model.portRange.start, self.port_data_model.portRange.end):
                self.thread_queue.append(portModel('', port, '', True, False))
            for port in reservedPortServices.get_all_reserved_port():
                self.thread_queue.append(port)

        elif self.task_type == portSniffingTask.application_port:
            for port in reservedPortServices.get_port_model():
                self.thread_queue.append(port)

    def execute_check_procedure(self):
        for port in range(0, self.port_data_model.thread_number):
            if self.thread_queue:
                port_model = self.thread_queue.pop()
                thread = Thread(target=self.check, args=(port_model,))
                thread.daemon = True
                self.excuting_thread.append(thread)
                thread.start()
                thread.join(0.01)
            else:
                break

    def check(self, port_model):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            flag = sock.connect_ex((self.port_data_model.address, port_model.port))
            if flag == 0:
                self.opened_port += 1
                if reservedPortServices.contains_port(port_model.port):
                    print("Port {} is open with {}".format(port_model.port, port_model.description))
                else:
                    print("Port {} is open".format(port_model.port))
            sock.close()
        except socket.gaierror:
            print("Hostname Could Not Be Resolved !!!!")
            return
        except socket.error:
            print("Server not responding!")
            return
        except KeyboardInterrupt:
            self.prompt_after_compeletion()
            exit(0)
        return

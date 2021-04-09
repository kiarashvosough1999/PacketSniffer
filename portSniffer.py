import socket
from threading import Thread
from Utilities.ThreadingUtilities import ThreadingUtilities
from Utilities.portManager import reservedPortServices


class portSniffer:

    def __init__(self, port_data_model):
        self.port_data_model = port_data_model
        socket.setdefaulttimeout(port_data_model.waitingTime)
        self.executing_thread = []
        self.ports_queue = []
        self.sniffing_mode = port_data_model.sniffing_mode
        self.open_ports = 0
        self.print_thread = ThreadingUtilities()

    def prompt_after_compeletion(self):
        if self.open_ports > 0:
            print('{} port{} opend'.format(self.open_ports, ' was' if self.open_ports <= 1 else 's were', ))
        else:
            print('no open ports in selcted mode found')

    def start(self):
        self.ports_queue = self.port_data_model.get_ports_by_mode()
        self.print_thread.start_print_thread()
        while self.ports_queue:
            count = 0
            for thread in self.executing_thread:
                if thread.is_alive():
                    count += 1
            if count == 0:
                self.executing_thread.clear()
                self.execute_check_procedure()
        self.prompt_after_compeletion()

    def execute_check_procedure(self):
        for port in range(0, self.port_data_model.thread_number):
            if self.ports_queue:
                port_model = self.ports_queue.pop(0)
                thread = Thread(target=self.check, args=(port_model,))
                thread.daemon = True
                self.executing_thread.append(thread)
                thread.start()
                thread.join(0.01)
            else:
                break

    def check(self, port_model):
        try:
            sock = socket.socket(self.port_data_model.ip_version, socket.SOCK_STREAM)
            connection_param = self.port_data_model.get_connect_param(port_model.port)
            flag = sock.connect_ex(connection_param)
            if flag == 0:
                self.open_ports += 1
                if reservedPortServices.contains_port(port_model.port):
                    self.print_thread.append_to_message(
                        "Port {} is open with {} and {}".format(port_model.port, port_model.description,
                                                                self.port_data_model.__str__()))
                else:
                    self.print_thread.append_to_message("Port {} is open {}".format(port_model.port, self.port_data_model.__str__()))
            # else:
            #     self.print_thread.append_to_message("Port {} is not open".format(port_model.port))
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

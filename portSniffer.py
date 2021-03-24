import socket
from threading import Timer, Thread


class portSniffer:

    def __init__(self, address, portRange, waitingTime, threadNum):
        self.address = str(address)
        self.portRange = portRange
        # self.waitingTime = waitingTime
        self.threadNum = threadNum
        self.last_port_check_attemp = portRange.start
        socket.setdefaulttimeout(waitingTime)
        self.excuting_thread = []
        self.end = False

    @staticmethod
    def get_reserved_port(port):
        dic = {'ftp': [21],
               'telnet': [23],
               'ssh': [22],
               'http': [80],
               'TLS HTTP' : [443],
               'smtp': [25, 465, 587],
               'SMTP & POP & IMAP With TLS': [993, 995, 465]
               }

        for key, value in dic.items():
            if value.__contains__(port):
                return key
        return ''

    @staticmethod
    def get_reserved_ports():
        return [21, 22, 23, 80, 25, 265, 287, 443, 993, 995, 465]

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

        end = self.last_port_check_attemp + self.threadNum
        start = self.last_port_check_attemp
        if end > self.portRange.end:
            end = self.portRange.end + 1
            self.end = True

        self.last_port_check_attemp += self.threadNum

        for port in range(start, end):
            thread = Thread(target=self.check, args=(port,))
            thread.daemon = True
            self.excuting_thread.append(thread)
            thread.start()
            thread.join(0.01)

    def check(self, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            flag = sock.connect_ex((self.address, port))
            if flag == 0:
                if self.get_reserved_ports().__contains__(port):
                    print("Port {} is open with {}".format(port, self.get_reserved_port(port)))
                else:
                    print("Port {} is open".format(port))
            # else:
            #     print("Port {} is not open".format(port))
            sock.close()
        except socket.gaierror:
            print("Hostname Could Not Be Resolved !!!!")
            return
        except socket.error:
            print("Server not responding !!!!")
            return
        except KeyboardInterrupt:
            exit(0)
        return

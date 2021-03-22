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

    def get_reserved_port(self, port):
        dic = {'ftp': [21], 'telnet': [23], 'ssh': [22], 'http': [80,443], 'smtp': [25, 465, 587]}
        for key, value in dic.items():
            if value.__contains__(port):
                return key
        return ''

    def get_reserved_ports(self):
        return [21, 22, 23, 80, 25, 265, 287, 443]

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
                self.check_and_execute()

    def check_and_execute(self):

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
            thread.join(0.1)

    def check(self, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            flag = sock.connect_ex((self.address, port))
            if flag == 0:
                if self.get_reserved_ports().__contains__(port):
                    print("Port {} is open with {}".format(port,self.get_reserved_port(port)))
                else:
                    print("Port {} is open".format(port))
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

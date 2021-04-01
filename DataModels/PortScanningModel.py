import socket

from DataModels.IPVersion import IPVersion


class PortScanningModel:

    def __init__(self, address, thread_number, portRange, waitingTime, task_type, ip_version=socket.AF_INET):
        self.address = address
        self.thread_number = thread_number
        self.portRange = portRange
        self.waitingTime = waitingTime
        self.ip_version = ip_version
        self.task_type = task_type

    def get_connect_param(self, port):
        if self.ip_version is socket.AF_INET6:
            return self.address, port, 0 , 0
        else:
            return self.address, port

    def __str__(self):
        return 'with ipV4' if self.ip_version is socket.AF_INET else 'with ipV6'

    def valid_ip_type(self):
        try:
            if self.ip_version is socket.AF_INET:
                self.address = socket.gethostbyname(self.address)
            else:
                address = socket.getaddrinfo(self.address,
                                             port=80,
                                             family=socket.AF_INET6,
                                             proto=socket.IPPROTO_TCP)
                if not address[0][4][0]:
                    return False
                self.address = address[0][4][0]
            # socket.inet_aton(self.address)
            return True
        except socket.error or socket.gaierror:
            return False

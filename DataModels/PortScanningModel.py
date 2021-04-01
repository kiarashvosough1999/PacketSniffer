import socket


class PortScanningModel:

    def __init__(self, address, thread_number, portRange, waitingTime, sniffing_mode, ip_version=socket.AF_INET):
        self.address = address
        self.thread_number = thread_number
        self.portRange = portRange
        self.waitingTime = waitingTime
        self.ip_version = ip_version
        self.sniffing_mode = sniffing_mode

    def get_connect_param(self, port):
        if self.ip_version is socket.AF_INET6:
            return self.address, port, 0, 0
        else:
            return self.address, port

    def __str__(self):
        return 'with ipV4' if self.ip_version is socket.AF_INET else 'with ipV6'

    def is_range_defined(self):
        if self.portRange.start == 1 and self.portRange.end == 1:
            return False
        return True

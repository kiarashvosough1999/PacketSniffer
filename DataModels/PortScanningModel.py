import socket


class PortScanningModel:

    def __init__(self, address, thread_number, portRange, waitingTime, task_type):
        self.address = address
        self.thread_number = thread_number
        self.portRange = portRange
        self.waitingTime = waitingTime
        self.ip_type = 0
        self.task_type = task_type

    def valid_ip_type(self):
        try:
            self.address = socket.gethostbyname(self.address)
            socket.inet_aton(self.address)
            return True
        except socket.error:
            return False

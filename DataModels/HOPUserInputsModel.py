import socket


class HOPUserInputsModel:

    def __init__(self,
                 max_ttl,
                 hop_tries,
                 packet_size,
                 waiting_time,
                 host_ipAddress=None,
                 host_address=None,
                 start_port=1,
                 start_ttl=0,
                 icmp_max_recv=1024):
        self.icmp_max_recv = icmp_max_recv
        if host_address:
            self.host_address = host_address
            self.host_ipAddress = socket.gethostbyname(host_address)
        else:
            self.host_ipAddress = host_ipAddress
            self.host_address = host_ipAddress
        self.start_port = start_port
        self.start_ttl = start_ttl
        self.max_ttl = max_ttl
        self.hop_tries = hop_tries
        self.packet_size = packet_size
        self.waiting_time = waiting_time

    def get_waiting_time_in_milisec(self):
        return self.waiting_time / 1000

    def get_port(self, ttl):
        if self.start_port and ttl - 2 > 1:
            return self.start_port
        else:
            return 1

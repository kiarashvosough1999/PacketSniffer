class TraceResponseModel:
    def __init__(self, receive_time,
                 recieved_packet_size=None,
                 reached_address=None,
                 icmp_header=None):
        self.receive_time = receive_time
        self.recieved_packet_size = recieved_packet_size - 28
        self.reached_address = reached_address
        self.icmp_header = icmp_header

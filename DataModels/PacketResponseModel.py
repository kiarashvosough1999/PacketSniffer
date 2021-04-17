class PacketResponseModel:

    def __init__(self, receive_time, recieved_packet_size, ip_header, icmp_header):
        self.receive_time = receive_time
        self.recieved_packet_size = recieved_packet_size - 28
        self.ip_header = ip_header
        self.icmp_header = icmp_header

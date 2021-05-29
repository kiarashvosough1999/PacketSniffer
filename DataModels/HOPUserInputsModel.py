
class HOPUserInputsModel:

    def __init__(self,
                 start_port,
                 start_ttl,
                 max_ttl,
                 hop_tries,
                 packet_size,
                 waiting_time):
        self.start_port = start_port
        self.start_ttl = start_ttl
        self.max_ttl = max_ttl
        self.hop_tries = hop_tries
        self.packet_size = packet_size
        self.waiting_time = waiting_time

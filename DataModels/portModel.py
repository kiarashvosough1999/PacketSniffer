
class portModel:

    def __init__(self, description, port, status, tcp, udp):
        self.description = description
        if type(port) is int:
            self.port = port
        else:
            self.port = int(port)
        self.status = status
        self.tcp = tcp
        self.udp = udp

    def __str__(self):
        return self.description + str(self.port)

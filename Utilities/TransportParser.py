from Utilities.Exception.MyExceptions import MyException


class TransportParser:

    def __init__(self, transport):
        self.transport = transport

    def get_socket(self):
        socket = self.transport.get_extra_info("socket")
        if socket:
            return socket
        else:
            raise MyException(message="error retrieving socket")

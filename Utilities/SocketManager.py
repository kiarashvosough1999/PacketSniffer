import select
import socket
from Utilities.ExceptionManager import ExceptionManager
from Utilities.MyExceptions import MyException


class socketManager:

    @staticmethod
    def get_tcp_stream_socket(ip_ver=socket.AF_INET):
        return socket.socket(ip_ver, socket.SOCK_STREAM)

    @staticmethod
    def get_tcp_raw_socket(ip_ver=socket.AF_INET):
        try:
            return socket.socket(ip_ver, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        except socket.error as error:
            raise ExceptionManager.handle_exception_raw_socket(error=error)

    @staticmethod
    def get_udp_raw_socket(ip_ver=socket.AF_INET):
        try:
            return socket.socket(ip_ver, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        except socket.error as error:
            raise ExceptionManager.handle_exception_raw_socket(error=error)

    @staticmethod
    def select_socket_with(sock, timeout):
        # wait until we can read sth from socket
        inputs = None
        if sock is not None:
            inputs, output, excepts = select.select([sock], [], [], timeout)
        if not inputs:
            raise MyException('packet could not be received',
                              error_type=MyException.packet_not_recieved)
        else:
            return input

import select
import socket
from DataModels.Constant import Constant
from Utilities.Exception.ExceptionManager import ExceptionManager
from Utilities.Exception.MyExceptions import MyException


class socketManager:

    @staticmethod
    def get_packet_socket(interface):
        if not interface:
            raise MyException(message="a interface should be picked")
        interface = interface[0:15]
        sock = None
        try:
            sock = socket.socket(family=socket.AF_PACKET,
                                 type=socket.SOCK_RAW,
                                 proto=0)
            sock.setblocking(False)
            try:
                sock.bind((interface, socket.SOCK_RAW))
            except OSError:
                raise MyException(message="error when attempting to bind")
        except socket.error as error:
            if sock:
                sock.close()
            raise ExceptionManager.handle_exception_raw_socket(error=error)
        return sock

    @staticmethod
    def get_tcp_icmp_raw_socket(ip_ver=socket.AF_INET, ttl=-1):
        try:
            sock = socket.socket(ip_ver, socket.SOCK_RAW, Constant.icmp_code)
            if ttl != -1:
                sock.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
            return sock
        except socket.error as error:
            raise ExceptionManager.handle_exception_raw_socket(error=error)

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

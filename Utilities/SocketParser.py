import fcntl
from ipaddress import IPv4Address
from struct import pack
from DataModels.Constant import Constant
from Utilities.Exception.MyExceptions import MyException


class SocketParser:

    def __init__(self, socket):
        self.socket = socket
        self._interface = None

    def parse(self):
        self._get_interface()
        return self._get_from_ioctl()

    def _get_from_ioctl(self):
        global ip, mac
        socket_descriptor = self.socket.fileno()
        info = fcntl.ioctl(socket_descriptor, Constant.SIOCSIFHWADDR, self._interface)
        if info[18:24]:
            mac = info[18:24]
        else:
            raise MyException(message="source mac can not be obtained")
        info = fcntl.ioctl(socket_descriptor, Constant.SIOCGIFADDR, self._interface)
        if IPv4Address(info[20:24]):
            ip = IPv4Address(info[20:24])
        else:
            raise MyException(message="source ip can not be obtained")
        return mac, ip

    def _get_interface(self):
        info = self.socket.getsockname()[0]
        if info:
            self._interface = pack("256s", info.encode("ascii"))
        else:
            raise MyException(message="cannot retrieve interface info")
import socket
import struct
from DataModels.Constant import Constant
from Utilities.MyExceptions import MyException


class ipHeaderModel:

    def __init__(self, ver, type, length, id, flags, ttl, protocol, checksum, source_ip):
        self.ver = ver
        self.type = type
        self.length = length
        self.id = id
        self.flags = flags
        self.ttl = ttl
        self.protocol = protocol
        self.checksum = checksum
        self.source_ip = source_ip

    def get_ip(self):
        return socket.inet_ntoa(struct.pack("!I", self.source_ip))

    def get_ttl(self):
        return self.ttl

    @staticmethod
    def get_ip_header_from_packet(packet, unpack_format=Constant.ip_header_format):

        ip = struct.unpack(unpack_format, packet[:20])
        if len(ip) >= 9:
            return ipHeaderModel(ip.__getitem__(0),
                                 ip.__getitem__(1),
                                 ip.__getitem__(2),
                                 ip.__getitem__(3),
                                 ip.__getitem__(4),
                                 ip.__getitem__(5),
                                 ip.__getitem__(6),
                                 ip.__getitem__(7),
                                 ip.__getitem__(8))
        return MyException("ip header of packet with id {} is coruppted".format(ip[3]),
                           error_type=MyException.corupted_ip_header)

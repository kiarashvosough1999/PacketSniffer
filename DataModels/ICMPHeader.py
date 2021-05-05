import struct
from DataModels.Constant import Constant
from Utilities.Exception.MyExceptions import MyException


class icmpHeader:

    def __init__(self, code, checksum, packet_id, sequence_number, unpack_format):
        self.code = code
        self.unpack_format = unpack_format
        self.checksum = checksum
        self.packet_id = packet_id
        self.sequence_number = sequence_number

    def received_packet_id(self):
        return self.packet_id

    @staticmethod
    def get_icmp_header_from_packet(packet, unpack_format=Constant.icmp_header_format):
        unpacked_header = struct.unpack(unpack_format, packet[20:28])

        if len(unpacked_header) >= 5:
            return icmpHeader(unpacked_header.__getitem__(1),  # code
                              unpacked_header.__getitem__(2),  # checksum
                              unpacked_header.__getitem__(3),  # packet_id
                              unpacked_header.__getitem__(4),  # sequence
                              unpacked_header.__getitem__(0))  # type
        raise MyException('packet header is corrupted',
                          error_type=MyException.corupted_icmp_header)

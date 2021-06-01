import random
import socket
import struct
import threading
from DataModels.Constant import Constant
from Ping.CheckSumUtilities import CheckSumFactory
from Ping.PaddingFactory import PaddingFactory


class PacketModel:

    def __init__(self,
                 destination_ip_address,
                 packet_size,
                 address='',
                 ip_ver=socket.AF_INET,
                 waiting_time=2,
                 icmp=8,
                 sequence_number=0,
                 pack_format=Constant.icmp_header_format,
                 packet_id=0):
        self.address = address
        self.waiting_time = waiting_time
        self.destination_ip_address = destination_ip_address
        self.icmp = icmp
        self._ipVer = ip_ver
        self.pack_format = pack_format
        self._id = packet_id
        self.sequence_number = sequence_number
        self.packet_size = packet_size

    def get_packet_id_based_on_thread(self):
        if self._id == 0:
            self._id = threading.current_thread().native_id & 0xFFFF
        return self._id

    def get_packet_id(self):
        return self._id

    def generate_random_id(self):
        self._id = int(random.random() * 65535)
        return self._id

    def create_packet(self):
        checksum = 0

        header = struct.pack(
            self.pack_format, self.icmp, 0, checksum, self._id, self.sequence_number
        )

        data = PaddingFactory(self.packet_size).get_padding_bytes()
        check_sum = CheckSumFactory(header + data)

        header = struct.pack(
            self.pack_format, self.icmp, 0, check_sum.get_checksum(), self._id, self.sequence_number
        )
        self.sequence_number += 1
        return header + data

    def create_packet_for_hop(self):
        header = struct.pack('bbHHh', self.icmp, 0, 0, self._id, 1)
        dummy_data = ''.encode('utf-8')
        checksum = CheckSumFactory(header + dummy_data).get_checksum_for_hop()
        header = struct.pack('bbHHh', self.icmp, 0, checksum, self._id, 1)
        return header + dummy_data

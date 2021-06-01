from socket import htons
from DataModels.Enums.ByteOrder import byteOrder
from DataModels.Constant import Constant
from Utilities.Exception.MyExceptions import MyException


class CheckSumFactory:

    def __init__(self, raw_packet_data):
        self.raw_packet_data = raw_packet_data
        self.raw_packet_length = int(len(raw_packet_data) / 2) * 2
        self.low_bytes = None
        self.high_bytes = None

    def get_checksum_for_hop(self):
        checksum_data = 0
        counter = 0
        while counter < self.raw_packet_length:
            this_val = (self.raw_packet_data[counter + 1]) * 256 + (self.raw_packet_data[counter])
            checksum_data = checksum_data + this_val
            checksum_data = checksum_data & 0xffffffff
            counter = counter + 2
        if self.raw_packet_length < len(self.raw_packet_data):
            checksum_data = checksum_data + (self.raw_packet_data[len(self.raw_packet_data) - 1])
            checksum_data = checksum_data & 0xffffffff
        checksum_data = (checksum_data >> 16) + (checksum_data & 0xffff)
        checksum_data = checksum_data + (checksum_data >> 16)
        res = ~checksum_data
        res = res & 0xffff
        res = res >> 8 | (res << 8 & 0xff00)
        return htons(res)

    def get_checksum(self):
        checksum_data = 0

        for index in range(0, self.raw_packet_length, 2):
            checksum_data += self.set_bytes(index)

        try:
            checksum_data += self.check_odd_bytes()
        except MyException as error:
            pass

        checksum_data &= Constant.hex_32bit_int
        checksum_data = (checksum_data >> 16) + (checksum_data & Constant.hex_16bit_int)
        checksum_data += (checksum_data >> 16)
        checksum = ~checksum_data & Constant.hex_16bit_int
        return htons(checksum)

    def check_odd_bytes(self):
        if self.raw_packet_length < len(self.raw_packet_data):
            bytes = self.raw_packet_data[len(self.raw_packet_data) - 1]
            return bytes
        raise MyException('not odd, its ok')

    def set_bytes(self, index):
        global high_bytes, low_bytes
        if Constant.bytes_order is byteOrder.little_endian:
            low_bytes = self.raw_packet_data[index]
            high_bytes = self.raw_packet_data[index + 1]
        else:
            low_bytes = self.raw_packet_data[index + 1]
            high_bytes = self.raw_packet_data[index]
        return high_bytes * 256 + low_bytes

    @staticmethod
    def get_packet_loss(sequence_number, packet_received):
        return (sequence_number - packet_received) / sequence_number * 100

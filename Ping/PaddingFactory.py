from DataModels.Constant import Constant


class PaddingFactory:

    def __init__(self, packet_size):
        self._packet_size = packet_size - 8

    def get_padding_bytes(self):
        padding_array = []
        for i in range(Constant.hex_66, Constant.hex_66 + self._packet_size):
            padding_array += [(i & Constant.hex_255)]
        return bytearray(padding_array)

from struct import pack

from Utilities.UseFullFunction import convert_int_to_bytes


class ARPPacketModel:

    def __init__(self, target, ip, mac):
        self.mac = mac
        self.ip = ip
        self.target = target

    def create_packet(self):
        packet = [
            pack("!6B", *(0xFF,) * 6),
            self.mac,
            pack("!H", 0x0806),
            pack("!HHBB", 0x0001, 0x0800, 0x0006, 0x0004),
            pack("!H", 0x0001),
            self.mac,
            convert_int_to_bytes(int(self.ip)),
            pack("!6B", *(0,) * 6),
            convert_int_to_bytes(int(self.target)),
        ]
        return b"".join(packet)

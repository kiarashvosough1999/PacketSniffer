from ipaddress import IPv4Address
import socket
from struct import unpack

from DataModels.Constant import Constant
from Utilities.Exception.MyExceptions import MyException


class EthernetResponseModel:

    def __init__(self, data, source_mac):
        self.data = data
        self.source_mac = source_mac

    def _parse_header(self):
        if self.data[0:14]:
            eth_header = self.data[0:14]
            return unpack(Constant.ARP_Header_format, eth_header)
        raise MyException(message="parsing arp response header failed")

    def _parse_detail(self):
        if self.data[14:42]:
            detail = self.data[14:42]
            return unpack(Constant.ARP_detail, detail)

    @staticmethod
    def _is_arp(flag):
        if not flag:
            raise MyException(message="error detecting arp header flag")
        return True if flag == Constant.ARP_flag else False

    def _send_for_this_device(self, detail):
        if detail[7] and detail[4]:
            return True if detail[4] == Constant.device_flag and detail[7] == self.source_mac else False
        raise MyException(message="error detecting response destination")

    @staticmethod
    def _parse_mac_address(detail):
        if detail:
            return ":".join(a + b for a, b in zip(*[iter(detail[5].hex())] * 2))
        raise MyException(message="error parsing mac from response")

    @staticmethod
    def _parse_ip_address(detail):
        if detail:
            str_format = socket.inet_ntoa(detail[6])
            return IPv4Address(str_format)
        raise MyException(message="error parsing ip from response")

    def parse_response(self):
        eth_detail = self._parse_header()
        if EthernetResponseModel._is_arp(eth_detail[2]):
            arp_detail = self._parse_detail()
            if self._send_for_this_device(detail=arp_detail):
                mac = EthernetResponseModel._parse_mac_address(arp_detail)
                ip = EthernetResponseModel._parse_ip_address(arp_detail)
                if ip:
                    print("IP address: ", ip)
                if mac:
                    print("MAC address: ", mac,
                          end="\n\n")
                return ip, mac

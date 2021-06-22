import asyncio
from DataModels.EthernetResponseModel import EthernetResponseModel
from Utilities.Exception.MyExceptions import MyException
from Utilities.TimeManager import TimeManager
from Utilities.TransportParser import TransportParser
from Utilities.SocketParser import SocketParser


class Arp(asyncio.Protocol):

    def __init__(self):
        self.transport = None
        self.request_model = None
        self.timer = None
        self._source_mac = None
        self._source_ip = None

    def connection_made(self, transport):
        self.transport = transport
        try:
            socket = TransportParser(transport=transport).get_socket()
            sock_parser = SocketParser(socket)
            #  save this computer ip and mac address
            #  mac is in binary format
            #  ip is human readable
            self._source_mac, self._source_ip = sock_parser.parse()
        except MyException as exception:
            print(exception.message)
            self.connection_lost(exception)
            exit(0)

    def connection_lost(self, exc):
        super(Arp, self).connection_lost(exc)
        try:
            sock = TransportParser(transport=self.transport).get_socket()
            if sock:
                sock.close()
        except MyException as excep:
            print(excep.message)
            exit(0)

    def send_arp_request(self, request_model):
        self.request_model = request_model
        self.request_model.set_source_info(mac=self._source_mac,
                                           ip=self._source_ip)
        self.timer = TimeManager(request_model.timeout)
        for packet in self.request_model.get_address_list():
            self.transport.write(packet.create_packet())

    def data_received(self, data):
        resp = EthernetResponseModel(data=data,
                                     source_mac=self.request_model.source_mac)
        if self.timer.is_timeout():
            self.connection_lost(MyException(message="time out occured"))
        try:
            resp.parse_response()
        except MyException as excep:
            print(excep.message)


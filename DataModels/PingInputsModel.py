from DataModels.PacketModel import PacketModel
from Utilities.Exception.MyExceptions import MyException, ExceptionAction
from Utilities.ValidationManager import ValidationManager


class PingInputsModel:

    def __init__(self, host_addresses, waiting_time, packet_size):
        self.host_addresses = host_addresses
        self.waiting_time = waiting_time
        self.packet_size = packet_size
        self.icmp_max_recv = 2048
        self.packet_models = []
        self.get_packet_models()

    def get_waiting_time_in_sec(self):
        return self.waiting_time / 1000

    def get_packet_models(self):
        for addr in self.host_addresses:
            try:
                address = ValidationManager.get_ip_from_address(address=addr)
                packet = PacketModel(addr,
                                     self.packet_size,
                                     waiting_time=self.waiting_time,
                                     address=addr)
                self.packet_models.append(packet)
            except MyException as error:
                print(error.message)
                continue
        if not self.packet_models:
            raise MyException('there is no host left to ping',
                              action=ExceptionAction.exit_0)



import json
import sys
from enum import Enum
from DataModels.PortModel import portModel


class reservedPortServices(Enum):
    TELNET = [23]
    FTP = [21]
    SSH = [22]
    HTTP = [80]
    HTTP_TLS = [443]
    SMTP = [25, 587]
    SMTP_TLS = [465]
    POP = [110]
    IMAP = [143]
    POP_TLS = [995]
    IMAP_TLS = [993]

    def describe(self):
        return self.name, self.value

    @staticmethod
    def decode_portModel(jsonObject):
        return portModel(jsonObject['description'],
                         int(jsonObject['port']),
                         jsonObject['status'],
                         jsonObject['tcp'],
                         jsonObject['udp'])

    @staticmethod
    def get_all_reserved_port():
        file_name = "Resourses/new_ports_data.json"
        try:
            read_file = open(file_name, 'r')
        except OSError:
            print("Could not open/read file:", file_name)
            sys.exit(0)

        with read_file:
            return json.load(read_file, object_hook=reservedPortServices.decode_portModel)

    # @staticmethod
    # def get_name(ports):
    #     return reservedPortServices(ports).name

    @classmethod
    def get_port_model(cls):
        list = []
        for row in cls:
            for num in row.value:
                get_name = lambda name: name + str(num) if len(row.value) > 1 else name
                list.append(portModel(get_name(row.name), num, 'Official', True, False))
        return list

    @classmethod
    def contains_port(cls, port):
        return [num for row in cls for num in row.value].__contains__(port)

from enum import Enum

from Utilities.Exception.MyExceptions import MyException


class AppMode(Enum):
    port_scanner = 1
    ping = 2
    arp = 4
    hop = 3

    @staticmethod
    def app_mode_from_int(input):
        if input == 1:
            return AppMode.port_scanner
        elif input == 2:
            return AppMode.ping
        elif input == 3:
            return AppMode.hop
        elif input == 4:
            return AppMode.arp
        else:
            raise MyException('app mode does not exist')

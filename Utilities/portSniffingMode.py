from enum import Enum
from Utilities.MyExceptions import MyException


class portSniffingMode(Enum):
    all_port = 0
    reserved_port = 1
    application_port = 2

    @staticmethod
    def get_type(from_string):
        if from_string == '1':
            return portSniffingMode.all_port
        elif from_string == '2':
            return portSniffingMode.reserved_port
        elif from_string == '3':
            return portSniffingMode.application_port
        raise MyExeption('Sniffing mode not found')

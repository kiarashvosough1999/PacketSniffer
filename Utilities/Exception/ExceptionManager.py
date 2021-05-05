import sys
from Utilities.Exception.MyExceptions import MyException


class ExceptionManager:

    @staticmethod
    def handle_exception_raw_socket(error):
        if error == 1:
            error_message = "Note that ICMP messages can only be send from processes running as root."
            return MyException(error_message,
                               error_type=MyException.socket_create_failed)
        else:
            type, value, traceback = sys.exc_info()
            error_message = str(value)
            return MyException(error_message,
                               error_type=MyException.socket_create_failed)

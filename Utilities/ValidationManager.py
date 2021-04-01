import socket

from Utilities.MyExceptions import ExeptionAction, MyExeption
from Utilities.customRange import customRange
from Utilities.portSniffingMode import portSniffingMode
from Utilities.UseFullFunction import safe_cast


class ValidationManager:

    @staticmethod
    def validate_ip_version(ip):
        if ip == '4':
            return socket.AF_INET
        elif ip == '6':
            return socket.AF_INET6
        else:
            raise MyExeption('ip vesrion not supported', ExeptionAction.continue_exec)

    @staticmethod
    def valid_ip_format(address, ip_version):
        try:
            if ip_version is socket.AF_INET:
                mAddress = socket.gethostbyname(address)
                return mAddress
            else:
                mAddress = socket.getaddrinfo(address,
                                             port=80,
                                             family=socket.AF_INET6,
                                             proto=socket.IPPROTO_TCP)
                if not mAddress[0][4][0]:
                    raise MyExeption('the host you requested for does not support ipV6',
                                     ExeptionAction.host_not_support_ipv6)
                return mAddress[0][4][0]
        except socket.gaierror:
            raise socket.gaierror
        except socket.error:
            raise socket.error

    @staticmethod
    def validate_userInput(address, thread_num, waiting_time, start, end, sniffing_mode, ip_version, max_thread):
        try:
            if not start or not end:
                mStart = 1
                mEnd = 1
            else:
                mStart = safe_cast(start, int, 'start')
                mEnd = safe_cast(end, int, 'end')
            mSniffing_mode = portSniffingMode.get_type(sniffing_mode)
            mThread_num = safe_cast(thread_num, int, 'thread number')
            if mThread_num >= max_thread:
                raise MyExeption('your computer only support {} thread concurently!!!'.format(max_thread))

            mWaiting_time = safe_cast(waiting_time, int, 'waiting time')
            mIP_version = ValidationManager.validate_ip_version(ip_version)
            mAddress = ValidationManager.valid_ip_format(address, mIP_version)

            return mAddress, mSniffing_mode, mThread_num, mWaiting_time, customRange(mStart, mEnd), mIP_version
        except MyExeption as e:
            raise e

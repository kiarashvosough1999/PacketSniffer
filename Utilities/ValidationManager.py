import socket
from ipaddress import IPv4Network, IPv4Address
from DataModels.ARPRequestModel import ARPRequestModel
from DataModels.Enums.AppMode import AppMode
from DataModels.HOPUserInputsModel import HOPUserInputsModel
from DataModels.customRange import customRange
from Utilities.Exception.MyExceptions import MyException, ExceptionAction
from Utilities.SystemInfo import SystemInfo
from Utilities.portSniffingMode import portSniffingMode
from Utilities.UseFullFunction import safe_cast


class ValidationManager:

    @staticmethod
    def validate_hop_info(max_ttl,
                          hop_tries,
                          packet_size,
                          waiting_time,
                          address,
                          start_port,
                          start_ttl):
        if 1 < start_port < 65535:
            raise MyException('start port must be in range 1..65535',
                              action=ExceptionAction.exit_0,
                              error_type=MyException.invalid_input)
        if start_ttl > 1:
            raise MyException('start ttl must be at least 1',
                              action=ExceptionAction.exit_0,
                              error_type=MyException.invalid_input)
        if waiting_time < 1000:
            raise MyException('waiting time must be greater than 1000, the unit is millisecond',
                              action=ExceptionAction.exit_0,
                              error_type=MyException.invalid_input)
        if max_ttl < 10:
            raise MyException('max ttl is less than enough',
                              error_type=MyException.invalid_input,
                              action=ExceptionAction.exit_0)
        if hop_tries < 3:
            raise MyException('hop tries is less than enough',
                              error_type=MyException.invalid_input,
                              action=ExceptionAction.exit_0)
        if packet_size < 0:
            raise MyException('waiting time must be greater than 0',
                              action=ExceptionAction.exit_0,
                              error_type=MyException.invalid_input)

        try:
            addr = ValidationManager.get_ip_from_address(address=address)
        except socket.gaierror:
            raise MyException('there is no valid host left to be pinged',
                              error_type=MyException.invalid_input,
                              action=ExceptionAction.exit_0)
        return HOPUserInputsModel(max_ttl=max_ttl,
                                  hop_tries=hop_tries,
                                  packet_size=packet_size,
                                  waiting_time=waiting_time,
                                  host_address=address,
                                  host_ipAddress=addr,
                                  start_port=start_port,
                                  start_ttl=start_ttl)

    @staticmethod
    def validate_app_mode(mode):
        try:
            int_mode = safe_cast(mode, int, 'can not detect app mode from input')
            app_mode = AppMode.app_mode_from_int(int_mode)
            return app_mode
        except MyException as error:
            print(error.message)
            error.do_action2()

    @staticmethod
    def get_ip_from_address(address):
        if ValidationManager.validate_ip_address(address):
            return address
        else:
            try:
                host = socket.gethostbyname(address)
                return host
            except socket.gaierror:
                raise MyException("ping: cannnot resolve {}: Unknown host".format(address))

    @staticmethod
    def validate_ip_address(address):
        try:
            socket.inet_aton(address)
            return True
        except socket.error:
            return False

    @staticmethod
    def validate_ip_version(ip):
        if ip == '4':
            return socket.AF_INET
        elif ip == '6':
            return socket.AF_INET6
        else:
            raise MyException('ip vesrion not supported', ExceptionAction.continue_exec)

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
                    raise MyException('the host you requested for does not support ipV6',
                                      ExceptionAction.host_not_support_ipv6)
                return mAddress[0][4][0]
        except socket.gaierror:
            raise socket.gaierror
        except socket.error:
            raise socket.error

    @staticmethod
    def validate_arp_user_inputs(start_ip, end_ip, waiting_time):
        domain, interface = SystemInfo.get_domain_and_interface()
        if not (start_ip and end_ip) and interface:  # no value from input
            return interface, ARPRequestModel(ip_list=IPv4Network(domain),
                                   timeout=waiting_time)
        elif start_ip and not end_ip and interface:  # mask
            return interface, ARPRequestModel(ip_list=IPv4Network(start_ip),
                                   timeout=waiting_time)
        elif start_ip and end_ip and interface:  # start and end ip provided by user
            return interface, ARPRequestModel(ip_list=[IPv4Address(start_ip),
                                            IPv4Address(end_ip)],
                                   timeout=waiting_time)
        else:
            raise MyException(message="there was no valid input or"
                                      " default value for this mode try again",
                              action=ExceptionAction.exit_0)

    @staticmethod
    def validate_ping_userInputs(max_thread, addreses, waiting_time, packet_size):
        pure_addresses = []
        if waiting_time < 1000:
            raise MyException('waiting time must be greater than 1000, the unit is millisecond',
                              action=ExceptionAction.exit_0,
                              error_type=MyException.invalid_input)
        if packet_size < 0:
            raise MyException('waiting time must be greater than 0',
                              action=ExceptionAction.exit_0,
                              error_type=MyException.invalid_input)
        for addr in addreses:
            try:
                ValidationManager.get_ip_from_address(address=addr)
                pure_addresses.append(addr)
            except socket.gaierror:
                print("ping: cannnot resolve {}: Unknown host, "
                      "this host will be removed from ping operation".format(addr))
                continue
        if len(pure_addresses) <= 0:
            raise MyException('there is no valid host left to be pinged',
                              error_type=MyException.invalid_input,
                              action=ExceptionAction.exit_0)
        elif len(pure_addresses) > max_thread:
            raise MyException('you\'ve reached the maximum number of host to be pinged,'
                              ' try again with the limit number prompted at the first for maximum thread',
                              error_type=MyException.invalid_input,
                              action=ExceptionAction.exit_0)
        return pure_addresses, waiting_time, packet_size

    @staticmethod
    def validate_userInput(address, thread_num, waiting_time, start, end, sniffing_mode, ip_version, max_thread):
        try:
            if not start or not end:
                mStart = 1
                mEnd = 1
            else:
                mStart = safe_cast(start, int, 'start')
                mEnd = safe_cast(end, int, 'end')
                if mStart <= 0 or mEnd <= 0:
                    raise MyException('selected range {}-{} is not valid'.format(mStart, mEnd))
            mSniffing_mode = portSniffingMode.get_type(sniffing_mode)
            mThread_num = safe_cast(thread_num, int, 'thread number')
            if mThread_num < 1:
                raise MyException('thread number is not valid, at least one thread should be applied')
            if mThread_num >= max_thread:
                raise MyException('your computer only support {} thread concurently!!!'.format(max_thread))

            mWaiting_time = safe_cast(waiting_time, int, 'waiting time')
            if mWaiting_time <= 0:
                raise MyException('waiting time can not be 0 or less than 0')
            mIP_version = ValidationManager.validate_ip_version(ip_version)
            mAddress = ValidationManager.valid_ip_format(address, mIP_version)

            return mAddress, mSniffing_mode, mThread_num, mWaiting_time, customRange(mStart, mEnd), mIP_version
        except MyException as e:
            raise e

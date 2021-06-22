from ipaddress import summarize_address_range, IPv4Address, IPv4Network
from Utilities.Exception.MyExceptions import MyException


class ARPRequestHelper:

    @staticmethod
    def construct_valid_ip_list(ip_list):
        if isinstance(ip_list, list):
            if len(ip_list) == 2:
                if ip_list[0] < ip_list[1]:  # this should be handled in validation
                    return summarize_address_range(ip_list[0],
                                                   ip_list[1])
        elif isinstance(ip_list, IPv4Address):
            return [ip_list]
        elif isinstance(ip_list, IPv4Network, ):
            return [ip_list]
        else:
            raise MyException(message="error parsing ip addresses")

    @staticmethod
    def is_Network(ip):
        return False if isinstance(ip, IPv4Address) else True

    @staticmethod
    def is_IPV4(ip):
        return True if isinstance(ip, IPv4Address) else False

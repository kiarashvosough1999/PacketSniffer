from DataModels.ARPPacketModel import ARPPacketModel
from Utilities.ARPRequestHelper import ARPRequestHelper
from Utilities.Exception.MyExceptions import MyException


class ARPRequestModel:

    def __init__(self, ip_list, timeout):
        self.ip_list = ip_list
        self.timeout = timeout
        self.source_ip = None
        self.source_mac = None
        self.ignore_ip_list = []

    def get_ip_mac(self):
        return self.source_ip, self.source_mac

    def add_skip_item(self, ip):
        if ip:
            self.ignore_ip_list.append(ip)

    def get_waiting_time_in_sec(self):
        return self.timeout / 1000

    def set_source_info(self, mac, ip):
        self.add_skip_item(ip)
        self.source_mac = mac
        self.source_ip = ip

    def should_ignore(self, ip):
        return True if ip in self.ignore_ip_list else False

    def set_timeout(self, lent):
        self.timeout = self.timeout * lent if lent > 0 else self.timeout

    def get_address_list(self):

        global valid_ip_list
        try:
            valid_ip_list = ARPRequestHelper.construct_valid_ip_list(ip_list=self.ip_list)
        except MyException as exce:
            print(exce.message)
            exit(0)
        models = []

        ipv4 = list(filter(ARPRequestHelper.is_IPV4, valid_ip_list))
        if ipv4:
            models = list(
                map(
                    self.filter_by_IPV4, ipv4
                )
            )
            self.set_timeout(len(models))
            return models

        networks = list(
            filter(
                ARPRequestHelper.is_Network,
                valid_ip_list
            )
        )

        if networks:
            # by networks hosts
            networks_hosts = []
            for item in networks:
                networks_hosts.extend(
                    list(
                        map(
                            lambda x: x,
                            item.hosts()
                        )
                    )
                )
            models += list(
                map(
                    self.filter_by_network_host, networks_hosts
                )
            )
            models += list(
                map(
                    self.filter_by_Network_address, networks
                )
            )
            models += list(
                map(
                    self.filter_by_broadcast_address, networks
                )
            )

            self.set_timeout(len(models))
            return list(
                filter(
                    lambda it: True if it else False,
                    models
                )
            )

    def filter_by_IPV4(self, addr):
        if not self.should_ignore(addr):
            return ARPPacketModel(target=addr,
                                  ip=self.source_ip,
                                  mac=self.source_mac)

    def filter_by_Network_address(self, addr):
        if addr.network_address not in self.ignore_ip_list:
            return ARPPacketModel(target=addr.network_address,
                                  ip=self.source_ip,
                                  mac=self.source_mac)

    def filter_by_broadcast_address(self, addr):
        if addr.broadcast_address not in self.ignore_ip_list:
            return ARPPacketModel(target=addr.broadcast_address,
                                  ip=self.source_ip,
                                  mac=self.source_mac)

    def filter_by_network_host(self, addr):
        if addr not in self.ignore_ip_list:
            return ARPPacketModel(target=addr,
                                  ip=self.source_ip,
                                  mac=self.source_mac)

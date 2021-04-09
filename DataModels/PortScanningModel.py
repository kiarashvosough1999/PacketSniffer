import socket
from DataModels.portModel import portModel
from Utilities.portManager import reservedPortServices
from Utilities.portSniffingMode import portSniffingMode


class PortScanningModel:

    def __init__(self, address, thread_number, portRange, waitingTime, sniffing_mode, ip_version=socket.AF_INET):
        self.address = address
        self.thread_number = thread_number
        self.portRange = portRange
        self.waitingTime = waitingTime
        self.ip_version = ip_version
        self.sniffing_mode = sniffing_mode

    def get_connect_param(self, port):
        if self.ip_version is socket.AF_INET6:
            return self.address, port, 0, 0
        else:
            return self.address, port

    def __str__(self):
        return 'with ipV4' if self.ip_version is socket.AF_INET else 'with ipV6'

    def is_range_defined(self):
        if self.portRange.start == 1 and self.portRange.end == 1:
            return False
        return True

    def get_all_ports(self):
        mapper1 = lambda port: portModel('', port, '', True, False)
        if self.is_range_defined():
            start = self.portRange.start
            end = self.portRange.end
        else:
            start = 0
            end = 65535
        ports = list(range(start, end))
        return list(map(mapper1, ports))

    def get_reserved_ports(self):
        ports = reservedPortServices.get_all_reserved_port()
        if self.is_range_defined():
            rec = lambda port: True if port in self.portRange.get_range() else False
            return list(filter(rec, ports)) + reservedPortServices.get_port_model()
        else:
            return ports + reservedPortServices.get_port_model()

    def get_application_port(self):
        ports = reservedPortServices.get_port_model()
        if self.is_range_defined():
            rec = lambda portMode: True if portMode.port in self.portRange.get_range() else False
            return list(filter(rec, ports))
        else:
            return ports

    def get_ports_by_mode(self):
        global ports
        if self.sniffing_mode == portSniffingMode.all_port:
            ports = self.get_all_ports()
        elif self.sniffing_mode == portSniffingMode.reserved_port:
            ports = self.get_reserved_ports()
        elif self.sniffing_mode == portSniffingMode.application_port:
            ports = self.get_application_port()
        ports.sort(key=lambda port: port.port)
        return ports

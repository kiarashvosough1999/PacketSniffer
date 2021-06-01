import socket
from DataModels.Constant import Constant
from DataModels.HOPTTLResponseDataModel import HOPTTLResponseDataModel
from DataModels.PacketModel import PacketModel
from DataModels.IcmpHeader import IcmpHeader
from DataModels.TraceResponseModel import TraceResponseModel
from Utilities.Exception.MyExceptions import MyException, ExceptionAction
from Utilities.SocketManager import socketManager
from Utilities.Threading.PrintThread import PrintThread
from Utilities.Threading.ThreadingUtilities import ThreadingUtilities
from Utilities.TimeManager import TimeManager


class TraceRouter:

    def __init__(self, hop_user_inputs_model):
        self.hop_user_inputs_model = hop_user_inputs_model
        self.destination_Address_found = False

    def start_hop(self):
        header = 'TraceRoute to {} <{}>   max hop tries: {}   max hop: {}  packet size:{} '.format(
            self.hop_user_inputs_model.host_address,
            self.hop_user_inputs_model.host_ipAddress,
            self.hop_user_inputs_model.max_ttl,
            self.hop_user_inputs_model.hop_tries,
            self.hop_user_inputs_model.packet_size
        )
        PrintThread.shared().append_to_message(Constant.Formatting.Blink +
                                               Constant.Color.F_Magenta +
                                               header +
                                               Constant.Formatting.Reset)
        for index in range(1, self.hop_user_inputs_model.max_ttl + 1):
            if self.start_ttl(index):
                self.destination_Address_found = True
                res = '<{}>'.format(self.hop_user_inputs_model.host_ipAddress) \
                      + ' was found!'
                PrintThread.shared().append_to_message(Constant.Formatting.Blink +
                                                       Constant.Color.F_Magenta +
                                                       res +
                                                       Constant.Formatting.Reset)
                ThreadingUtilities.wait(3)
                break

    def start_ttl(self, ttl):
        responseParser = HOPTTLResponseDataModel()
        for tr in range(1, self.hop_user_inputs_model.hop_tries + 1):
            try:
                responseParser.set_last_try(tr)
                sock = socketManager.get_tcp_icmp_raw_socket(ttl=ttl)
                packet = PacketModel(destination_ip_address=self.hop_user_inputs_model.host_ipAddress,
                                     packet_size=self.hop_user_inputs_model.packet_size,
                                     waiting_time=self.hop_user_inputs_model.waiting_time,
                                     sequence_number=ttl,
                                     pack_format=Constant.icmp_header_format2)
                packet.generate_random_id()
                sending_time = self.send_packet(sock=sock,
                                                packet_model=packet)

                packet_response = self.receive(sock=sock,
                                               packet_model=packet)
                responseParser.save_delay(sending_time, packet_response.receive_time)
                sock.close()
                if packet_response and packet_response.reached_address:
                    responseParser.append_response(packet_response)
                    break
            except MyException as error:
                continue
        if ttl == 2:
            responseParser.print_gateway()
        elif ttl > 2 and self.hop_user_inputs_model.start_ttl < ttl - 2:
            responseParser.print_sequential_result(ttl - 2)
        return responseParser.reached_ip_Address == self.hop_user_inputs_model.host_ipAddress

    def send_packet(self, sock, packet_model):

        packet = packet_model.create_packet_for_hop()
        time = TimeManager().get_time()
        port = self.hop_user_inputs_model.get_port(packet_model.sequence_number)
        try:
            z = sock.sendto(packet, (packet_model.destination_ip_address, port))
        except socket.error as e:
            raise MyException(message="General failure ({})".format(e.args[1]),
                              action=ExceptionAction.no_action,
                              error_type=MyException.failure)

        return time

    def receive(self, sock, packet_model):
        timeout = self.hop_user_inputs_model.get_waiting_time_in_milisec()
        time = TimeManager(timeout)
        while True:
            try:
                # wait for socket receive sth so that we can read it
                # socketManager.select_socket_with(socket, timeout)
                socketManager.select_socket_with(sock, timeout)
            except MyException as error:
                raise error
            packet, address = sock.recvfrom(self.hop_user_inputs_model.icmp_max_recv)

            # waiting time is reached, no need to continue,
            # packet may be lost or gone for holiday
            time.capture_elapsed_time()
            if time.is_timeout():
                raise MyException('Request timeout for icmp_seq {}'.format(packet_model.sequence_number),
                                  error_type=MyException.timeout)
            # get icmp header model from byte array received from socket
            icmp_header = IcmpHeader.get_icmp_header_from_packet_for_hop(packet)
            receive_time = TimeManager.get_time()
            if icmp_header.received_packet_id() == packet_model.get_packet_id():
                packet_response = TraceResponseModel(receive_time=receive_time,
                                                     recieved_packet_size=len(packet),
                                                     reached_address=address[0],
                                                     icmp_header=icmp_header)
                return packet_response

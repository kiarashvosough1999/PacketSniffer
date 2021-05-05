import socket
from threading import Thread
from time import sleep
from DataModels.PacketResponseModel import PacketResponseModel
from DataModels.PingResponseModel import PingResponseModel
from Utilities.Exception.MyExceptions import MyException, ExceptionAction
from DataModels.ICMPHeader import icmpHeader
from DataModels.IPHeaderModel import ipHeaderModel
from Utilities.SocketManager import socketManager
from Utilities.Threading.ThreadingUtilities import ThreadingUtilities
from Utilities.TimeManager import timeManager


class ping:

    def __init__(self, ping_inputs_model):
        self.ping_inputs_model = ping_inputs_model
        self.thread_list = []
        self.stop = False

    def start(self):

        for packet in self.ping_inputs_model.packet_models:
            thread = Thread(target=self.start_ping,
                                      args=(packet,))

            thread.daemon = True
            thread.start()
            self.thread_list.append(thread)
            thread.join(0.01)
        try:
            ThreadingUtilities.shared().keep_main_thread_alive()
        except KeyboardInterrupt:
            self.stop = True
            ThreadingUtilities.wait_for_threads(self.thread_list,
                                                should_sleep=5)

    def start_ping(self, packet_model):
        sock = None
        identifier = packet_model.get_packet_id_based_on_thread()
        response = PingResponseModel(identifier=identifier)
        while not self.stop:
            try:
                # get raw socket to send packet | raise -> socket_create_failed
                sock = socketManager.get_tcp_raw_socket()
                # send packet to the destination ip address,
                # return time in sec | raise -> ping_failed
                sending_time = self.send_packet(sock=sock,
                                                packet_model=packet_model)

                # receive packet from the destination ip address,
                # return PacketResponseModel | raise -> timeout | packet_not_received
                packet_response = self.receive(sock=sock,
                                               packet_model=packet_model)
                sock.close()
                # calculate delay from sending and receiving

                response.save_delay(sending_time=sending_time,
                                    receive_time=packet_response.receive_time)

                # storing updated packet model
                response.set_next_packet_model(packet_model)
                # print statistic for user
                response.print_sequential_result(packet_response=packet_response)
                # wait for next ping
                sleep(1.7)
            except MyException as error:
                if sock:
                    sock.close()
                if error.error_type is MyException.ping_failed:
                    # print(error.message)
                    response.print_sending_error()
                    continue
                elif error.error_type is MyException.socket_create_failed:
                    print(error.message)
                    return
                elif error.error_type is MyException.packet_not_recieved:
                    response.print_not_received()
                    continue
                elif error.error_type is MyException.timeout:
                    response.print_timeout()
                    continue
                elif error.error_type is (MyException.corupted_icmp_header or MyException.corupted_ip_header):
                    continue
                elif error.error_type is MyException.failure:
                    print(error.message)
                    error.do_action()
                    return

        response.print_final_result()

    @staticmethod
    def send_packet(sock, packet_model):
        # return packet bytearray, and increment sequence number
        packet = packet_model.create_packet()
        elapsed_time = timeManager.get_time()
        # send packet to the destination host
        try:
            z = sock.sendto(packet, (packet_model.destination_ip_address, 1))
        except socket.error as e:
            raise MyException(message="General failure ({})".format(e.args[1]),
                              action=ExceptionAction.exit_0,
                              error_type=MyException.failure)
        if not elapsed_time:
            raise MyException('sending packet failed',
                              error_type=MyException.ping_failed)
        return elapsed_time

    def receive(self, sock, packet_model):

        timeout = self.ping_inputs_model.get_waiting_time_in_sec()
        while True:
            time = timeManager(timeout)
            try:
                # wait for socket receive sth so that we can read it
                # socketManager.select_socket_with(socket, timeout)
                socketManager.select_socket_with(sock, timeout)
            except MyException as error:
                raise error

            # get received data from socket
            packet, address = sock.recvfrom(self.ping_inputs_model.icmp_max_recv)
            # get icmp header model from byte array received from socket
            icmp_header = icmpHeader.get_icmp_header_from_packet(packet, packet_model.pack_format)

            receive_time = timeManager.get_time()

            # if the received packet id is as the same as the packet id that we've sent,
            # then it it desired response
            # for that sent packet
            if icmp_header.received_packet_id() == packet_model.get_packet_id_based_on_thread():
                # get ip header model from byte array received from socket
                ip_header_model = ipHeaderModel.get_ip_header_from_packet(packet)
                packet_response = PacketResponseModel(receive_time=receive_time,
                                                      recieved_packet_size=len(packet),
                                                      ip_header=ip_header_model,
                                                      icmp_header=icmp_header)

                return packet_response
            # waiting time is reached, no need to continue,
            # packet may be lost or gone for holiday
            if time.is_timeout():
                raise MyException('Request timeout for icmp_seq {}'.format(packet_model.sequence_number),
                                  error_type=MyException.timeout)

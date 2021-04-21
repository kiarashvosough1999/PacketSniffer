from DataModels.Constant import Constant
from Ping.CheckSumUtilities import CheckSumFactory
from Utilities import TimeManager
from Utilities.Threading.PrintThread import PrintThread
from functools import reduce


class PingResponseModel:

    def __init__(self, identifier):
        self.identifier = identifier
        self.packet_model = None
        self.delays = []

    def print_final_result(self):
        self.get_analyzes()
        header = "\n------------------------------ <{}({})> statistics ----------------------".format(
            self.packet_model.destination_ip_address,
            self.packet_model.address)
        body = "\n<{}> packets sent, <{}> packets received, {:.1f}% packet loss".format(
            self.packet_model.sequence_number,
            self.get_received_packet(),
            CheckSumFactory.get_packet_loss(sequence_number=self.packet_model.sequence_number,
                                            packet_received=self.get_received_packet())
        )
        max_rtt, min_rtt, avg_rtt = self.get_analyzes()
        footer = "\nRTT: min=<{:.3f}>ms   avg=<{:.3f}>ms   max=<{:.3f}>ms\n".format(
            min_rtt,
            avg_rtt,
            max_rtt
        )
        PrintThread.shared().append_to_message(Constant.Formatting.Bold +
                                               Constant.Color.F_LightMagenta +
                                               header + body + footer + Constant.Color.F_Default)

    def print_sequential_result(self, packet_response):
        body = "{} bytes from IP<{}({})> seq={} ttl={} in {:.3f} ms".format(
            packet_response.recieved_packet_size,
            packet_response.ip_header.get_ip(),
            self.packet_model.address,
            self.packet_model.sequence_number,
            packet_response.ip_header.get_ttl(),
            self.delays[-1]
        )
        PrintThread.shared().append_to_message(Constant.Formatting.Blink +
                                               Constant.Color.F_LightGreen +
                                               body + Constant.Color.F_Default + Constant.Formatting.Reset)

    def print_timeout(self):
        if not self.packet_model:
            body = "request to {}({}) timeout -> seq={}".format(
                self.packet_model.destination_ip_address,
                self.packet_model.address,
                self.packet_model.sequence_number
            )
            PrintThread.shared().append_to_message(Constant.Formatting.Bold +
                                                   Constant.Color.F_Red +
                                                   body +
                                                   Constant.Formatting.Reset +
                                                   Constant.Color.F_Default)

    def print_not_received(self):
        if not self.packet_model:
            body = "response from {}({}) not received -> seq={}".format(
                self.packet_model.destination_ip_address,
                self.packet_model.address,
                self.packet_model.sequence_number
            )
            PrintThread.shared().append_to_message(Constant.Formatting.Bold +
                                                   Constant.Color.F_Red +
                                                   body +
                                                   Constant.Formatting.Reset +
                                                   Constant.Color.F_Default)

    def get_received_packet(self):
        return len(self.delays)

    def save_delay(self, sending_time,  receive_time):
        delay = TimeManager.timeManager.get_delay_in_sec(sending_time,receive_time)
        self.delays.append(delay)

    def set_next_packet_model(self,packet_model):
        self.packet_model = packet_model

    def get_analyzes(self):
        max_rtt = max(self.delays) if self.delays else 0.0
        min_rtt = min(self.delays) if self.delays else 0.0
        avg_rtt = reduce(lambda a, b: a + b, self.delays) / self.get_received_packet() if self.delays else 0.0
        return max_rtt, min_rtt, avg_rtt

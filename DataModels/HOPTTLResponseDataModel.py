from DataModels.Constant import Constant
from Utilities import TimeManager
from Utilities.Threading.PrintThread import PrintThread


class HOPTTLResponseDataModel:

    def __init__(self):
        self.reached_ip_Address = ''
        self.delays = 0.0
        self.didTry = 0

    def append_response(self, response):
        self.reached_ip_Address = response.reached_address

    def set_last_try(self, didTry):
        self.didTry = didTry

    def save_delay(self, sending_time, receive_time):
        delay = TimeManager.TimeManager.get_delay_in_sec(sending_time, receive_time)
        self.delays = delay

    def print_gateway(self):
        res = 'GateWay to <{}> after 0 tries'.format(self.reached_ip_Address)
        PrintThread.shared().append_to_message(Constant.Formatting.Blink +
                                               Constant.Color.F_Cyan +
                                               res +
                                               Constant.Formatting.Reset)

    def print_sequential_result(self, ttl):
        if self.delays != 0 and self.reached_ip_Address != '':
            final_result_text = 'HOP<{}>'.format(ttl) + \
                                '    <==>  ' + \
                                '<{}>'.format(self.reached_ip_Address) + \
                                ' in ' + \
                                "{:.3f} ms".format(self.delays) + \
                                ' after ' + \
                                '{} tries'.format(self.didTry)
            PrintThread.shared().append_to_message(Constant.Formatting.Blink +
                                                   Constant.Color.F_Green
                                                   + final_result_text +
                                                   Constant.Formatting.Reset)
        else:
            res = 'HOP<{}>'.format(ttl) + \
                  '    <==> ' + \
                  ' NO REPLY after ' + \
                  '{} tries'.format(self.didTry)
            PrintThread.shared().append_to_message(Constant.Formatting.Blink +
                                                   Constant.Color.F_Red +
                                                   res + Constant.Formatting.Reset)

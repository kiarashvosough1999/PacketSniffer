from enum import Enum


class ExceptionAction(Enum):
    exit_0 = 0
    continue_exec = 1
    break_exec = 2
    no_action = -1
    host_not_support_ipv6 = 21


class MyException(Exception):
    corupted_icmp_header = -1
    corupted_ip_header = -3
    failure = -2
    ping_failed = -4
    timeout = -5
    socket_create_failed = -6
    packet_not_recieved = -7
    none = 0
    casting_error = -10
    invalid_input = -20

    def __init__(self, message, action=ExceptionAction.no_action, error_type=0):
        self.message = message
        self.action = action
        self.error_type = error_type

    def __str__(self):
        return self.message

    def do_action2(self):
        if self.action == ExceptionAction.exit_0:
            exit(0)

    def do_action(self):
        if self.error_type == MyException.failure:
            exit(0)

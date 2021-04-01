from enum import Enum


class ExeptionAction(Enum):
    exit_0 = 0
    continue_exec = 1
    break_exec = 2
    no_action = -1
    casting_error = 10
    host_not_support_ipv6 = 21


class MyExeption(Exception):
    def __init__(self, message, action=ExeptionAction.no_action):
        self.message = message
        self.action = action

    def __str__(self):
        return self.message

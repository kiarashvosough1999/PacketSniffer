import subprocess

from DataModels.Constant import Constant
from Utilities.Exception.MyExceptions import MyException


class SystemInfo:

    @staticmethod
    def get_ifconfig():
        return [
            x
            for x in subprocess.getoutput(
                Constant.ifconfig_re_expression
            ).split(" ")
            if x
        ]

    @staticmethod
    def get_domain_and_interface():
        info = SystemInfo.get_ifconfig()
        if info[0]:
            domain = info[0]
        else:
            raise MyException(message="your domain not found, try to connect to a network")
        if info[2]:
            interface = info[2]
        else:
            raise MyException(message="default interface not found")
        return domain, interface

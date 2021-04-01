# PortScanningModel(socket.gethostbyname('142.250.179.206'), 2, customRange(70, 450),1)
import socket

from DataModels.IPVersion import IPVersion
from Utilities.AppStartManager import AppStartManager

if __name__ == '__main__':
    AppStartManager().start()
    # l = socket.getaddrinfo("www.pythonhlk.org", 443, family=socket.AF_INET6, proto=socket.IPPROTO_TCP)
    # if l[0][4][0]:
    #     print(l[0][4][0])
    # sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    # flag = sock.connect_ex(("::ffff:151.101.12.223", 80, 0, 0))
    # if flag == 0:
    #     print("done")
    #
    # def bound_socket(*a, **k):
    #     sock = socket.socket(*a, **k)
    #     if socket.AF_INET6 in a:
    #         if not socket.has_ipv6:
    #             raise ValueError("There's no support for IPV6!")
    #         else:
    #             address = [addr for addr in socket.getaddrinfo(l, None)
    #                        if socket.AF_INET6 == addr[0]]  # You ussually want the first one.
    #             if not address:
    #                 raise ValueError("Couldn't find ipv6 address for source %s" % l)
    #             sock.bind(address[0][-1])
    #     else:
    #         sock.bind((l, 0))
    #     return sock
    #
    # bound_socket()
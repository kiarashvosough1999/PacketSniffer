# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import os
import ssl

from customRange import customRange
from portSniffer import portSniffer
import sys
import socket

#     # Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # try:
        x = portSniffer(socket.gethostbyname('142.250.179.206'), customRange(437, 450), 2, 6)
        x.start()
    # except KeyboardInterrupt:
    #     print('\tInterrupted')
    #     sys.exit(0)

    # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # flag = sock.connect_ex(('uk2.sshagan.us', 22))
    # if flag == 0:
    #     print("Port {} is open".format(22))
    # else:
    #     print("Port {} is not open".format(22))
    # sock.close()

    # print(socket.getaddrinfo("www.python.org", 80, 0, 0, socket.SOL_TCP))

    # hostname = 'vu.um.ac.ir'
    # context = ssl.create_default_context()
    #
    # with socket.create_connection(('uk2.sshagan.us', 443)) as sock:
    #     with context.wrap_socket(sock, server_hostname=hostname) as ssock:
    #         print(ssock.version())


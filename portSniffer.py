import sys
import socket
import threading
from datetime import datetime


class portSniffer:

    def __init__(self, address, portRange, waitingTime, threadNum):
        self.address = str(address)
        self.portRange = portRange
        self.waitingTime = waitingTime
        self.threadNum = threadNum

    def start(self):
        for port in self.portRange:
            x = threading.Thread(target=self.check, args=(port,))
            x.start()

    def check(self, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(1)
            flag = sock.connect_ex((self.address, port))
            if flag == 0:
                print("Port {} is open".format(port))
            # else:
            #     print("Port {} is not open".format(port))
            sock.close()
        except socket.gaierror:
            print("\n Hostname Could Not Be Resolved !!!!")
            # return
        except socket.error:
            print("\nServer not responding !!!!")
            # return
        # return

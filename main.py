
from Utilities.customRange import customRange
from portSniffer import portSniffer
import sys
import socket

if __name__ == '__main__':
    try:
        x = portSniffer(socket.gethostbyname('142.250.179.206'), customRange(70, 450), 2, 6)
        x.start()
    except KeyboardInterrupt:
        print('\tInterrupted')
        sys.exit(0)

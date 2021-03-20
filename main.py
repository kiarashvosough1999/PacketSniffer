# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import os

from customRange import customRange
from portSniffer import portSniffer
import sys
import socket

#     # Press the green button in the gutter to run the script.
if __name__ == '__main__':
    try:
        x = portSniffer(socket.gethostbyname('142.250.179.206'), customRange(430, 450), 2, 6)
        x.start()
    except KeyboardInterrupt:
        print('\tInterrupted')
        sys.exit(0)


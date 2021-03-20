# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from portSniffer import portSniffer
import sys
import socket


#     # Press the green button in the gutter to run the script.
if __name__ == '__main__':
    x = portSniffer(socket.gethostbyname('142.250.179.206'), range(1, 500), 5, 6)
    x.start()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

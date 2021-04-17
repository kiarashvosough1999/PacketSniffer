import socket
from enum import Enum


class IPVersion(Enum):
    v4 = socket.AF_INET
    v6 = socket.AF_INET6

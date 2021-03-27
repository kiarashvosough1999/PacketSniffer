from enum import Enum


class reservedPortServices(Enum):
    TELNET = [23]
    FTP = [21]
    SSH = [22]
    HTTP = [80]
    HTTP_TLS = [443]
    SMTP = [25, 587]
    SMTP_TLS = [465]
    POP = [110]
    IMAP = [143]
    POP_TLS = [995]
    IMAP_TLS = [993]

    def describe(self):
        return self.name, self.value

    @staticmethod
    def get_name(ports):
        return reservedPortServices(ports).name

    @classmethod
    def contains_port(cls,port):
        return [num for row in cls for num in row.value].__contains__(port)

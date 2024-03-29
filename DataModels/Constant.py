import sys
from DataModels.Enums.ByteOrder import byteOrder
import socket


class Constant:
    hex_255 = 0xff
    hex_66 = 0x42
    hex_16bit_int = 0xffff
    hex_32bit_int = 0xffffffff
    icmp_header_format = "!BBHHH"
    icmp_header_format2 = "bbHHh"
    ip_header_format = "!BBHHHBBHII"
    icmp_code = socket.getprotobyname('icmp')

    ifconfig_re_expression = "ip route|sed '/via/d' |sed '/docker/d'|sed '/linkdown/d'|sed '/src /!d' | sed '/dev /!d' |sed '2,$d'"

    big_byte_order = "big"

    socket = "socket"
    s256 = "256s"

    device_flag = b"\x00\x02"
    ARP_detail = "2s2s1s1s2s6s4s6s4s"
    ARP_Header_format = "!6s6s2s"
    ARP_flag = b"\x08\x06"
    SIOCGIFADDR = 0x8915  # C flag to obtain ip address of the system
    SIOCSIFHWADDR = 0x8927  # C flag to obtain mac address of the system

    bytes_order = byteOrder.little_endian if sys.byteorder == "little" else byteOrder.big_endian

    class Base:
        # Foreground:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        # Formatting
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
        # End colored text
        END = '\033[0m'
        NC = '\x1b[0m'  # No Color

    class Formatting:
        Bold = "\x1b[1m"
        Dim = "\x1b[2m"
        Italic = "\x1b[3m"
        Underlined = "\x1b[4m"
        Blink = "\x1b[5m"
        Reverse = "\x1b[7m"
        Hidden = "\x1b[8m"
        # Reset part
        Reset = "\x1b[0m"
        Reset_Bold = "\x1b[21m"
        Reset_Dim = "\x1b[22m"
        Reset_Italic = "\x1b[23m"
        Reset_Underlined = "\x1b[24"
        Reset_Blink = "\x1b[25m"
        Reset_Reverse = "\x1b[27m"
        Reset_Hidden = "\x1b[28m"

    class Color:
        # Foreground
        F_Default = "\x1b[39m"
        F_Black = "\x1b[30m"
        F_Red = "\x1b[31m"
        F_Green = "\x1b[32m"
        F_Yellow = "\x1b[33m"
        F_Blue = "\x1b[34m"
        F_Magenta = "\x1b[35m"
        F_Cyan = "\x1b[36m"
        F_LightGray = "\x1b[37m"
        F_DarkGray = "\x1b[90m"
        F_LightRed = "\x1b[91m"
        F_LightGreen = "\x1b[92m"
        F_LightYellow = "\x1b[93m"
        F_LightBlue = "\x1b[94m"
        F_LightMagenta = "\x1b[95m"
        F_LightCyan = "\x1b[96m"
        F_White = "\x1b[97m"
        # Background
        B_Default = "\x1b[49m"
        B_Black = "\x1b[40m"
        B_Red = "\x1b[41m"
        B_Green = "\x1b[42m"
        B_Yellow = "\x1b[43m"
        B_Blue = "\x1b[44m"
        B_Magenta = "\x1b[45m"
        B_Cyan = "\x1b[46m"
        B_LightGray = "\x1b[47m"
        B_DarkGray = "\x1b[100m"
        B_LightRed = "\x1b[101m"
        B_LightGreen = "\x1b[102m"
        B_LightYellow = "\x1b[103m"
        B_LightBlue = "\x1b[104m"
        B_LightMagenta = "\x1b[105m"
        B_LightCyan = "\x1b[106m"
        B_White = "\x1b[107m"

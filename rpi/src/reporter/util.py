import time
import socket
import fcntl
import struct
import rpi.src.server.handlers.util as handlerutil

__gps_last_load_time = 0  # initialize to 0 so we reload when we start up
__gps_location = None
__gps_reload_duration = 300  # 5 minutes


def __load_gps_location():
    try:
        with open(handlerutil.GPS_LOCATION, "r") as f:
            location = f.read()
            return location
    except FileNotFoundError:
        return None


def get_gps_location():
    global __gps_location
    now = time.time()
    if __gps_location is None or now - __gps_last_load_time > __gps_reload_duration:
        __gps_location = __load_gps_location()
        __gps_load_time = now

    return __gps_location


def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', bytes(ifname[:15], "utf-8"))
    )[20:24])

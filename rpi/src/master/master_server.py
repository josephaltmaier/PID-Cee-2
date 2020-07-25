import socket

import socket, struct, fcntl

MASTER_PORT = 17403
# Mesh network has no built in DNS so hard-code the master IP address for now.
MASTER_ADDRESS = "192.168.0.69"

SIOCSIFADDR = 0x8916


def start():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        setIpAddr(serversocket, "bat0", MASTER_ADDRESS)
        serversocket.bind((socket.gethostname(), MASTER_PORT))
        serversocket.listen(5)

        while True:
            sock = serversocket.accept()
    finally:
        serversocket.close()


def setIpAddr(sock, iface, ip):
    bin_ip = socket.inet_aton(ip)
    ifreq = struct.pack('16sH2s4s8s', bytes(iface, "utf-8"), socket.AF_INET, bytes('\x00' * 2, "utf-8"), bin_ip, bytes('\x00' * 8, "utf-8"))
    fcntl.ioctl(sock, SIOCSIFADDR, ifreq)


if __name__ == "__main__":
    start()

import socket
import struct
import fcntl
import time
import rpi.src.shared.util as util
from rpi.src.generated.proto.mesh_pb2 import NodeReport
from concurrent.futures import ThreadPoolExecutor

MASTER_PORT = 17403
# Mesh network has no built in DNS so hard-code the master IP address for now.
MASTER_ADDRESS = "192.168.0.69"

SIOCSIFADDR = 0x8916

# 5 second timeout for all socket operations
TIMEOUT = 5


def start():
    threadPool = ThreadPoolExecutor(3)
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        #  TODO: the interface (bat0) and probably the port should be passed in as an argument.  Can also get rid of the
        #  hard-coded IP address if we add some kind of DNS.service
        __set_ip_addr(serversocket, "bat0", MASTER_ADDRESS)
        serversocket.bind((MASTER_ADDRESS, MASTER_PORT))
        serversocket.listen(5)

        while True:
            sock, address = serversocket.accept()
            print("Accepted connection from", address)
            threadPool.submit(__handle_client_sock, sock)
    finally:
        serversocket.close()


def __set_ip_addr(sock, iface, ip):
    bin_ip = socket.inet_aton(ip)
    ifreq = struct.pack('16sH2s4s8s', bytes(iface, "utf-8"), socket.AF_INET, bytes('\x00' * 2, "utf-8"), bin_ip,
                        bytes('\x00' * 8, "utf-8"))
    fcntl.ioctl(sock, SIOCSIFADDR, ifreq)


def __handle_client_sock(sock):
    sock.settimeout(TIMEOUT)

    sizeBytes = __get_exact_bytes(sock, 4)
    messageSize = int.from_bytes(sizeBytes, "big")  # bytes from the network should always be big endian
    print("receiving a message of %d bytes", (messageSize))

    messageBytes = __get_exact_bytes(sock, messageSize)
    message = NodeReport()
    message.ParseFromString(messageBytes)
    print(message)


def __get_exact_bytes(sock, numBytes):
    startTime = time.time()
    receivedBytes = []
    while len(receivedBytes < numBytes):
        if time.time() - startTime > 5:
            raise TimeoutError("Timeout exceeded waiting for data")
        numBytesToGet = numBytes - len(receivedBytes)
        moreBytes = sock.recv(numBytesToGet)
        receivedBytes = receivedBytes + moreBytes
    if len(receivedBytes) != numBytes:
        raise ValueError("We should have exactly %d bytes for message size.  Instead read %d bytes",
                         (numBytes, len(receivedBytes)))
    return receivedBytes


if __name__ == "__main__":
    start()

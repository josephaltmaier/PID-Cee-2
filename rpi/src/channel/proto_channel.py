import time
import rpi.src.server.util as util


class ProtoChannel():
    def __init__(self, sock):
        self.sock = sock

    def recv(self):
        print("Waiting for size from client")
        sizeBytes = self.__get_exact_bytes(4)
        messageSize = int.from_bytes(sizeBytes, "big")  # bytes from the network should always be big endian
        print("receiving a message of %d bytes" % messageSize)

        return self.__get_exact_bytes(messageSize)

    def send(self, proto):
        sendBytes = proto.SerializeToString()
        msgSize = len(sendBytes)
        if len(sendBytes) > util.ONE_MB:
            raise ValueError("Cannot send message, size %d is larger than max size %d", (msgSize, util.ONE_MB))

        networkOrderMsgSize = (msgSize).to_bytes(4, byteorder='big')
        self.sock.sendall(networkOrderMsgSize)
        self.sock.sendall(sendBytes)

    def __get_exact_bytes(self, numBytes):
        startTime = time.time()
        receivedBytes = bytearray()
        while len(receivedBytes) < numBytes:
            if time.time() - startTime > 5:
                raise TimeoutError("Timeout exceeded waiting for data")

            numBytesToGet = numBytes - len(receivedBytes)
            print("Getting %d bytes" % (numBytesToGet))
            moreBytes = self.sock.recv(numBytesToGet)

            print("Got %d bytes" % (len(moreBytes)))
            receivedBytes = receivedBytes + moreBytes
        if len(receivedBytes) != numBytes:
            raise ValueError("We should have exactly %d bytes for message size.  Instead read %d bytes",
                             (numBytes, len(receivedBytes)))
        return receivedBytes

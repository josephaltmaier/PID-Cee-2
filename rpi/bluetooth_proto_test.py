import threading
from google.protobuf.any_pb2 import Any
from rpi.src.generated.proto.bluetooth_pb2 import HelloWorld
import bluetooth

def receiveAndRespond(socket):
    try:
        data = client_sock.recv(1024)
        print("Data received:", str(data))
        testAny = Any()
        testAny.ParseFromString(data)

        testHW = HelloWorld()
        testAny.Unpack(testHW)
        responseMessage = data
        if testHW.message:
            print("Received proto message:", testHW.message)
            responseMessage = testHW.message
        else:
            print("Received non-proto message")

        responseHW = HelloWorld()
        responseHW.message = "Received message:" + responseMessage

        responseWrapper = Any()
        responseWrapper.Pack(responseHW)
        responseBytes = responseWrapper.SerializeToString()
        socket.send(responseBytes)
    finally:
        socket.close()

server_sock = bluetooth.BluetoothSocket(bluetooth.L2CAP)

port = 0x24067

server_sock.bind(("", port))
server_sock.listen(1)

try:
    while True:
        client_sock, address = server_sock.accept()
        print("Accepted connection from", address)
        t = threading.Thread(target=receiveAndRespond, args=(client_sock,))
        t.setDaemon(True)
        t.start()
finally:
    server_sock.close()

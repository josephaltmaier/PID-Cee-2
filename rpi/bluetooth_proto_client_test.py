import sys

import bluetooth
from rpi.src.generated.proto.bluetooth_pb2 import HelloWorld
from google.protobuf.any_pb2 import Any


sock = bluetooth.BluetoothSocket(bluetooth.L2CAP)

if len(sys.argv) < 2:
    print("Usage: l2capclient.py <addr>")
    sys.exit(2)

bt_addr = sys.argv[1]
port = 0x24067

print("Trying to connect to {} on PSM 0x{}...".format(bt_addr, port))

sock.connect((bt_addr, port))

print("Connected. Type something...")
while True:
    data = input()
    if not data:
        break

    hello = HelloWorld()
    hello.message = data
    any = Any()
    any.Pack(hello)
    protoString = any.SerializeToString()

    sock.send(protoString)
    data = sock.recv(1024)
    print("Data received:", str(data))

sock.close()

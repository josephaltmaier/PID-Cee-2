import bluetooth
import traceback
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from rpi.src.generated.proto.bluetooth_pb2 import Request, Response
from google.protobuf.timestamp_pb2 import Timestamp

__threadPool = ThreadPoolExecutor(3)

__listenerLock = Lock()
__handlers = []

__oneMB = 1 << 20
__maxErrorSize = 1000000

__timeout = 5000  # I think timeout is in milliseconds


def addHandler(listenerFunc):
    with __listenerLock:
        __handlers .append(listenerFunc)


def start(port):
    server_sock = bluetooth.BluetoothSocket(bluetooth.L2CAP)
    server_sock.bind(("", port))
    server_sock.listen(1)

    try:
        while True:
            client_sock, address = server_sock.accept()
            print("Accepted connection from", address)
            __threadPool.submit(__handle_client_sock, client_sock)
    finally:
        server_sock.close()


def __handle_client_sock(sock):
    request = None
    try:
        request = __get_request(sock)
        response = __handle_request(request)
        __send_response(sock, response)
    except Exception as e:
        traceback.print_exc()
        response = __make_error_response(e, request.request_id if request else None)
        try:
            __send_response(sock, response)
        except:
            pass  # Already printed the first exception, this one is of limited value.
    finally:
        sock.close()


def __make_error_response(e, request_id):
    response = Response()
    response.request_id = request_id
    response.time = Timestamp().GetCurrentTime()
    response.succeeded = False
    response.error = str(e)
    # __maxErrorSize leaves ~48k for overhead.  This error message shouldn't be anywhere near 1MB anyway.
    if len(response.error) > __maxErrorSize:
        response.error = response.error[:__maxErrorSize]
    return response


def __get_request(sock):
    sock.settimeout(__timeout)
    messageBytes = sock.recv(__oneMB)
    request = Request()
    request.ParseFromString(messageBytes)
    return request


def __handle_request(request):
    for handler in __handlers:
        response = handler.handle(request)
        if not response:
            continue
        response.time = Timestamp().GetCurrentTime()
        response.request_id = request.request_id
        response.succeeded = True
        return response # One handler per request, first handler to respond wins
    raise ValueError("No handler for request")


def __send_response(sock, response):
    responseBytes = response.SerializeToString()
    if len(responseBytes) > __oneMB:
        e = ValueError("response too long, %s bytes", (len(responseBytes)))
        response = __make_error_response(e, response.request_id)
        responseBytes = response.SerializeToString()
    sock.send(responseBytes)

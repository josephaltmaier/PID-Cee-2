import bluetooth
import traceback
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from rpi.src.generated.proto.bluetooth_pb2 import Request, Response, ResponseContext
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
        response = __make_error_response(e, request.request_context.request_id if request else None)
        try:
            print("Sending error response")
            __send_response(sock, response)
        except Exception as innerException:
            print("Failed to send error response due to %s", str(innerException))
    finally:
        sock.close()


def __make_error_response(e, request_id):
    response = Response()
    response.response_context = ResponseContext()
    response.response_context.request_id = request_id
    response.response_context.time = Timestamp().GetCurrentTime()
    response.response_context.succeeded = False
    response.response_context.error = str(e)
    # __maxErrorSize leaves ~48k for overhead.  This error message shouldn't be anywhere near 1MB anyway.
    if len(response.response_context.error) > __maxErrorSize:
        response.response_context.error = response.response_context.error[:__maxErrorSize]
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
        response.response_context = ResponseContext()
        response.response_context.time = Timestamp().GetCurrentTime()
        response.response_context.request_id = request.request_context.request_id
        response.response_context.succeeded = True
        return response # One handler per request, first handler to respond wins
    raise ValueError("No handler for request")


def __send_response(sock, response):
    responseBytes = response.SerializeToString()
    if len(responseBytes) > __oneMB:
        e = ValueError("response too long, %s bytes", (len(responseBytes)))
        response = __make_error_response(e, response.response_context.request_id)
        responseBytes = response.SerializeToString()
    sock.send(responseBytes)

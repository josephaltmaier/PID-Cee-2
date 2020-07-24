from rpi.src.generated.proto.bluetooth_pb2 import Response
from google.protobuf.timestamp_pb2 import Timestamp

ONE_MB = 1 << 20
MAX_ERROR_SIZE = 1000000


def make_error_response(e, request_id):
    response = Response()
    response.response_context.request_id = request_id
    response.response_context.time.GetCurrentTime()
    response.response_context.succeeded = False
    response.response_context.error = str(e)
    # __maxErrorSize leaves ~48k for overhead.  This error message shouldn't be anywhere near 1MB anyway.
    if len(response.response_context.error) > MAX_ERROR_SIZE:
        response.response_context.error = response.response_context.error[:MAX_ERROR_SIZE]
    return response

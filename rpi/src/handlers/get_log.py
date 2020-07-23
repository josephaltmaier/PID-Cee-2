from rpi.src.generated.proto.bluetooth_pb2 import Response, LOG
import rpi.src.handlers.util as util

class GetLogHandler:
    def handle(self, request):
        if not request.getter:
            return None
        if request.getter != LOG:
            return None

        log = util.getLog()

        response = Response()
        response.log = log
        return response

def validate_location(location):
    return True

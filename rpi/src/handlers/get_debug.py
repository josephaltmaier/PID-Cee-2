from rpi.src.generated.proto.bluetooth_pb2 import Response, Debug, DEBUG
import rpi.src.handlers.util as util

class GetDebugHandler:
    def handle(self, request):
        if not request.getter:
            return None
        if request.getter != DEBUG:
            return None

        debug = Debug()
        debug.config = util.getConfig()
        debug.log = util.getLog()
        debug.mesh_info = util.getMeshInfo()
        debug.known_beacons = util.getKnownBeacons()

        response = Response()
        response.debug = debug
        return response

def validate_location(location):
    return True

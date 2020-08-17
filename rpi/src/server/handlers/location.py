from rpi.src.generated.proto.bluetooth_pb2 import Response
import rpi.src.server.handlers.util as util

class SetLocationHandler:
    def handle(self, request):
        if not request.location:
            return None

        newLocation = request.location.gps_location
        if not validate_location(newLocation):
            raise ValueError("Invalid location: %s", str(newLocation))

        with open(util.GPS_LOCATION, "w") as locFile:
            locFile.write(str(newLocation))

        response = Response()
        response.location = request.location
        return response

def validate_location(location):
    return True

from rpi.src.generated.proto.bluetooth_pb2 import Response, Config, CONFIG
import rpi.src.handlers.util as util

class GetConfigHandler:
    def handle(self, request):
        if not request.getter:
            return None
        if request.getter != CONFIG:
            return None

        location = util.getLocation()
        btConfig = util.getBluetoothConfig()
        config = Config()
        config.location = location
        config.bluetooth_config = btConfig

        response = Response()
        response.config = config
        return response

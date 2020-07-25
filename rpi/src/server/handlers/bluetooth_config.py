from rpi.src.generated.proto.bluetooth_pb2 import Response

class SetBluetoothConfigHandler:
    def handle(self, request):
        if not request.bluetooth_config:
            return None

        newConfig = request.bluetooth_config
        if not validate_config(newConfig):
            raise ValueError("invalid bluetooth configuration: ", str(newConfig))
        # TODO: figure out how to change the advertised bluetooth name
        response = Response()
        response.bluetooth_config = newConfig
        return response


def validate_config(config):
    return True

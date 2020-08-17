from rpi.src.generated.proto.bluetooth_pb2 import Config, Location, BluetoothConfig, Log, MeshInfo, KnownBeacons

GPS_LOCATION = "gps_location"

def getLocation():
    location = Location()
    try:
        with open(GPS_LOCATION, "r") as f:
            location.location = float(f.read())
    except:
        pass
    return location


def getBluetoothConfig():
    btConfig = BluetoothConfig()
    # TODO: Figure out how to get the advertised bluetooth name
    return btConfig

def getConfig():
    config = Config()
    config.location = getLocation()
    config.bluetooth_config = getBluetoothConfig()
    return config

def getLog():
    log = Log()
    # TODO: Implement logging then add the last 1mb of logs here
    log.log = "Joseph Rules!"
    return log

def getMeshInfo():
    meshInfo = MeshInfo()
    # TODO: Figure out how to get the mesh network info
    return meshInfo

def getKnownBeacons():
    beacons = KnownBeacons()
    # TODO: Either scan for beacons or report the results of the most recent scan??
    return beacons

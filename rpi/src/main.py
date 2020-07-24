import rpi.src.server.bluetooth_server as bluetooth_server
from rpi.src.handlers import bluetooth_config, get_debug, get_log, get_config, location

PORT = 0x24067


def main():
    bluetooth_server.addHandler(bluetooth_config.SetBluetoothConfigHandler())
    bluetooth_server.addHandler(get_debug.GetDebugHandler())
    bluetooth_server.addHandler(get_log.GetLogHandler())
    bluetooth_server.addHandler(get_config.GetConfigHandler())
    bluetooth_server.addHandler(location.SetLocationHandler())
    bluetooth_server.start(PORT)


if __name__ == "__main__":
    main()
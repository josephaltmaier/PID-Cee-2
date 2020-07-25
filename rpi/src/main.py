import threading
import uuid
import time
import rpi.src.server.bluetooth_server as bluetooth_server
import rpi.src.reporter.reporter as reporter
from rpi.src.server.handlers import get_debug, get_config, location, bluetooth_config, get_log

API_PORT = 24067
MASTER_PORT = 17403
# Mesh network has no built in DNS so hard-code the master IP address for now.
MASTER_ADDRESS = "192.168.0.69"


def main(): # TODO: Run these as processes and restart them when they fail
    apiThread = __start_bluetooth_api()
    reporterThread = __start_reporter()

    while True:
        # make sure the threads are running every minute
        time.sleep(60)
        if not apiThread.is_alive():
            print("API thread has died, shutting down the node")
            return
        if not reporterThread.is_alive():
            print("Reporter thread has died, shutting down the node")
            return


def __start_bluetooth_api():
    bluetooth_server.addHandler(bluetooth_config.SetBluetoothConfigHandler())
    bluetooth_server.addHandler(get_debug.GetDebugHandler())
    bluetooth_server.addHandler(get_log.GetLogHandler())
    bluetooth_server.addHandler(get_config.GetConfigHandler())
    bluetooth_server.addHandler(location.SetLocationHandler())
    apiThread = threading.Thread(target=bluetooth_server.start, args=[API_PORT, ])
    apiThread.setDaemon(True)
    apiThread.start()
    return apiThread


def __start_reporter():
    reporterThread = threading.Thread(target=reporter.start, args=[__get_id(), MASTER_ADDRESS, MASTER_PORT, ])
    reporterThread.setDaemon(True)
    reporterThread.start()
    return reporterThread


def __get_id():
    try:
        with open("node_id", "r") as f:
            nodeID = f.read()
    except FileNotFoundError:
        with open("node_id", "w") as f:
            nodeID = uuid.uuid4()
            f.write(nodeID)

    return nodeID


if __name__ == "__main__":
    main()

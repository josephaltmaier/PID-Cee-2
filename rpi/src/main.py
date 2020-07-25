import threading
import uuid
import time
import rpi.src.server.bluetooth_server as bluetooth_server
import rpi.src.reporter.reporter as reporter
from rpi.src.handlers import bluetooth_config, get_debug, get_log, get_config, location

PORT = 0x24067


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
    apiThread = threading.Thread(target=bluetooth_server.start, args=[PORT, ])
    apiThread.setDaemon(True)
    apiThread.start()
    return apiThread


def __start_reporter():
    # TODO: store and reuse the ID, get a real master address and filter func
    fakeNodeID = uuid.uuid4()
    reporterThread = threading.Thread(target=reporter.start, args=[fakeNodeID, "fakeIP", "fakePort", ])
    reporterThread.setDaemon(True)
    reporterThread.start()
    return reporterThread


if __name__ == "__main__":
    main()

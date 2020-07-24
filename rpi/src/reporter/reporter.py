import socket
import time
import sys
import rpi.src.reporter.scanner as scanner
import rpi.src.reporter.util as util
from rpi.src.generated.proto.mesh_pb2 import NodeReport

def start(id, masterAddress, masterPort, filter):
    while True:
        time.sleep(10)
        s = None
        try:
            gpsLocation = util.get_gps_location()
            if gpsLocation is None:
                continue

            tagReports = scanner.scan(filter)
            print("Detected %s ble devices", len(tagReports))
            print(tagReports)
            if len(tagReports) == 0:
                continue

            nodeReport = NodeReport()
            nodeReport.node_id = id
            nodeReport.time.GetCurrentTime()
            nodeReport.gps_location = gpsLocation
            nodeReport.tag_reports = tagReports
            reportBytes = nodeReport.SerializeToString()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((masterAddress, masterPort))
            # network is in big endian byte order
            networkOrderMessageLen = (len(reportBytes)).to_bytes(4, byteorder='big')
            s.sendall(networkOrderMessageLen)
            s.sendall(reportBytes)
        finally:
            if s:
                s.close()

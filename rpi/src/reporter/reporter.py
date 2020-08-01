import socket
import time
import rpi.src.reporter.scanner as scanner
import rpi.src.reporter.util as util
import rpi.src.shared.util as sharedUtil
from rpi.src.generated.proto.mesh_pb2 import NodeReport


def start(id, master_address, master_port, filter_func=None):
    while True:
        time.sleep(10)
        s = None
        try:
            gpsLocation = util.get_gps_location()
            if gpsLocation is None:
                print("GPS location not set, sleeping")
                continue

            tagReports = scanner.scan(filter_func)
            print("Detected %s ble devices", len(tagReports))
            print(tagReports)
            if len(tagReports) == 0:
                print("No ble devices detected, sleeping")
                continue

            nodeReport = NodeReport()
            nodeReport.node_id = str(id)
            nodeReport.time.GetCurrentTime()
            nodeReport.gps_location = gpsLocation
            nodeReport.tag_reports.extend(tagReports)
            reportBytes = nodeReport.SerializeToString()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ipaddress = sharedUtil.get_ip_address("bat0")
            s.bind((ipaddress, 0))
            s.connect((master_address, master_port))
            # network is in big endian byte order
            networkOrderMessageLen = (len(reportBytes)).to_bytes(4, byteorder='big')
            s.sendall(networkOrderMessageLen)
            s.sendall(reportBytes)
        except ConnectionRefusedError:
            print("Could not connect to master")
        finally:
            if s:
                s.close()

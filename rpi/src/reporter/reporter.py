import socket
import time
import traceback
import rpi.src.reporter.scanner as scanner
import rpi.src.reporter.util as util
from rpi.src.generated.proto.mesh_pb2 import NodeReport
from rpi.src.channel.proto_channel import ProtoChannel


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
            print("Detected %s ble devices" % len(tagReports))
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
            #  TODO: This behavior should be encapsulated in the channel
            ipaddress = util.get_ip_address("bat0")
            s.bind((ipaddress, 0))
            s.connect((master_address, master_port))
            channel = ProtoChannel(s)
            channel.send(reportBytes)
        except ConnectionRefusedError:
            print("Could not connect to master")
        except:
            traceback.print_exc()
        finally:
            if s:
                s.close()

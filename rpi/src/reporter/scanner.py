from bluetooth.ble import BeaconService
from rpi.src.generated.proto.mesh_pb2 import TagReport

service = BeaconService()


def scan(filter_func):
    devices = service.scan(2)

    tagProtos = []
    for address, data in list(devices.items()):
        report = TagReport()
        report.tag_id = data[0]
        report.major = data[1]
        report.minor = data[2]
        report.power = data[3]
        report.rssi = data[4]
        report.address = address
        report.propagation_constant = 2  # TODO: make this tunable or even dynamic.  It depends on the interference between the beacon and the receiver.
        # TODO: figure out how to get a state
        if filter_func is None or filter_func(report):
            tagProtos.append(report)

    return tagProtos

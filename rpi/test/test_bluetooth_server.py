import unittest
import rpi.src.bluetooth_server as blueooth_server


class TestBluetoothServer(unittest.TestCase):

    def test_error_response(self):
        testError = ValueError("test error")
        errResponse = blueooth_server.__make_error_response(testError, "test")
        print(errResponse)


if __name__ == '__main__':
    unittest.main()

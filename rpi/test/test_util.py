import unittest
import rpi.src.server.util as util


class TestBluetoothServer(unittest.TestCase):

    def test_error_response(self):
        testError = ValueError("test error")
        errResponse = util.make_error_response(testError, "test")
        self.assertIsNotNone(errResponse.response_context)
        self.assertEqual("test", errResponse.response_context.request_id)
        self.assertIsNotNone(errResponse.response_context.time)
        self.assertFalse(errResponse.response_context.succeeded)
        self.assertEqual("test error", errResponse.response_context.error)

    def test_error_response_without_id(self):
        testError = ValueError("test error")
        errResponse = util.make_error_response(testError, None)
        self.assertIsNotNone(errResponse.response_context)
        self.assertIsNone(errResponse.response_context.request_id)
        self.assertIsNotNone(errResponse.response_context.time)
        self.assertFalse(errResponse.response_context.succeeded)
        self.assertEqual("test error", errResponse.response_context.error)


if __name__ == '__main__':
    unittest.main()

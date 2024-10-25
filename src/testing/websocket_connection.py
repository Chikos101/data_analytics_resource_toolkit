import unittest
from websocket_connection import *
import websocket
from utilities import generate_auth_header
import ssl
import json
config_file = open('config.json')
config = json.load(config_file)
class TestWebsocketConnection(unittest.TestCase):
    def test_websocket_connection(self):

        # call the function for testing
        output = websocket_request(config)
        
        self.assertIsInstance(output, websocket._core.WebSocket)


if __name__ == '__main__':
    unittest.main()

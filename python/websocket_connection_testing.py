import unittest
from unittest.mock import patch, Mock
from websocket_connection import websocket_request
import websocket
from utilities import generate_auth_header
import ssl
import json
config_file = open('config.json')
config = json.load(config_file)
class TestWebsocketConnection(unittest.TestCase):
    @patch('websocket.create_connection')
    def test_websocket_connection(self,  mock_get):
        response_type = websocket._core.WebSocket
        mock_get.return_value.type = response_type
        output = websocket_request(config)
        print(output)
        mock_get.assert_called_with(config['websocket_url'],
                       sslopt={"cert_reqs": ssl.CERT_NONE},
                       header = [f"Authorization: {generate_auth_header(config)}"])
        self.assertIsInstance(output, response_type)


if __name__ == '__main__':
    unittest.main()

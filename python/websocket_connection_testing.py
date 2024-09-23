import unittest
from unittest.mock import patch, MagicMock
from websocket_connection import *
import websocket
from utilities import generate_auth_header
import ssl
import json
config_file = open('config.json')
config = json.load(config_file)
class TestWebsocketConnection(unittest.TestCase):
    @patch('websocket.create_connection')
    @patch('utilities.generate_auth_header')
    def test_websocket_connection(self,  mock_gen_auth, mock_websocket):
        # setup mock for websocket
        mock_ws = MagicMock()
        mock_websocket.return_value = mock_ws

        #simulate real-time headers for helper function
        mock_gen_auth.return_value = ' Bearer access token'

        # call the function for testing
        output = websocket_request(config)

        # assert the websocket connection was created with real-time headers
        mock_websocket.assert_called_with(config['websocket_url'],
                       sslopt={"cert_reqs": ssl.CERT_NONE},
                       header = [f"Authorization: Bearer access token"])
        
        # assert the helper function was called with the correct real-time arguments
        mock_gen_auth.asser_called_with(config)
        self.assertIsInstance(output, websocket._core.WebSocket)


if __name__ == '__main__':
    unittest.main()

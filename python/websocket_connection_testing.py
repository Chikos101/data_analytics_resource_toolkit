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
        mock_gen_auth.return_value = ' Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6ImIxbE9sa1ptd2x0bUVFbVY2TXU2dl9kRmJ5QSIsInBpLmF0bSI6IjEifQ.eyJzY29wZSI6W10sImNsaWVudF9pZCI6IkFQSV9FNDY1NjhfUFJPRCIsImF1ZCI6IlByb2QiLCJqdGkiOiI3MTRCN1RsTjRvUmpiTGRiIiwic3ViIjoiQVBJX0U0NjU2OF9QUk9EIiwiZXhwIjoxNzI3MTI3MjgyfQ.ZKaSd4ZVmQG1UQ6sHjZi-pl_L9eHTEW1hlinMLBOIx4AqHJmyZ-pZkGRmIZcI2ihiyNEqLE0K8gUwEkx_xPrQbXcpv0c9WhKQQDWbOmffcr54kzpfDvh1RwjTSnJzjyXNSF1_e4jmywzOzim9uqHCm9jD1vznHWkEBeBoLrQfCLNhpC-3lvZwzkvPVkcpHFC5aMZRWIM11pE3DmyZ_91QNKeO9-NUkXwm5w49-SOGFzrjKWmt6ctbeqmEp04XMdMTOXIKlmp8GRE23Pqcsh6ozMHKhSr8I-JRqHGXw9mYXhowRzXv1YgUBIKF5uC6iwUXWpsDFMgHR8dIZg655oUfQ'

        # call the function for testing
        output = websocket_request(config)

        # assert the websocket connection was created with real-time headers
        mock_websocket.assert_called_with(config['websocket_url'],
                       sslopt={"cert_reqs": ssl.CERT_NONE},
                       header = [f"Authorization: Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6ImIxbE9sa1ptd2x0bUVFbVY2TXU2dl9kRmJ5QSIsInBpLmF0bSI6IjEifQ.eyJzY29wZSI6W10sImNsaWVudF9pZCI6IkFQSV9FNDY1NjhfUFJPRCIsImF1ZCI6IlByb2QiLCJqdGkiOiI3MTRCN1RsTjRvUmpiTGRiIiwic3ViIjoiQVBJX0U0NjU2OF9QUk9EIiwiZXhwIjoxNzI3MTI3MjgyfQ.ZKaSd4ZVmQG1UQ6sHjZi-pl_L9eHTEW1hlinMLBOIx4AqHJmyZ-pZkGRmIZcI2ihiyNEqLE0K8gUwEkx_xPrQbXcpv0c9WhKQQDWbOmffcr54kzpfDvh1RwjTSnJzjyXNSF1_e4jmywzOzim9uqHCm9jD1vznHWkEBeBoLrQfCLNhpC-3lvZwzkvPVkcpHFC5aMZRWIM11pE3DmyZ_91QNKeO9-NUkXwm5w49-SOGFzrjKWmt6ctbeqmEp04XMdMTOXIKlmp8GRE23Pqcsh6ozMHKhSr8I-JRqHGXw9mYXhowRzXv1YgUBIKF5uC6iwUXWpsDFMgHR8dIZg655oUfQ"])
        
        # assert the helper function was called with the correct real-time arguments
        mock_gen_auth.asser_called_with(config)
        self.assertIsInstance(output, websocket._core.WebSocket)


if __name__ == '__main__':
    unittest.main()

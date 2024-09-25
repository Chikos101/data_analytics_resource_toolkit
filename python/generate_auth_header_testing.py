from utilities import generate_auth_header
import unittest
from unittest.mock import patch, Mock
import requests
import json

config_file = open('config.json')
config = json.load(config_file)


class TestGenerateAuthHeader(unittest.TestCase):
    @patch('requests.post')
    def test_generate_auth_header(self, mock_get):
        response = generate_auth_header(config)
        mock_get.assert_called_with(config["auth_url"], data={'grant_type': 'client_credentials'},
                              auth=(config["client_id"], config["client_secret"]))
        self.assertIsInstance(response, str)
        

if __name__ == '__main__':
    unittest.main()


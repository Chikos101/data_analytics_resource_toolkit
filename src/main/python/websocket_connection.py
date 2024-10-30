from websocket import create_connection
from utilities import *

"""
    Creates a WebSocket connection.

    Args:
        config (json): the json representation of the config file

    Returns:
        WebSocket: The websocket object that can be used to examine market data
"""
def websocket_request(config):
    validate_config(config)
    websocket_url = config["websocket_url"]
    ws = create_connection(websocket_url,
                    #    sslopt={"cert_reqs": ssl.CERT_NONE},
                       header = [f"Authorization: {generate_auth_header(config)}"])
    
    return ws
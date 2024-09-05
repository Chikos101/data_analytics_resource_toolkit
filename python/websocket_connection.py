from websocket import create_connection
import ssl
from utilities import *

"""
    Creates a WebSocket connection.

    Returns:
        WebSocket: The websocket object that can be used to examine market data
"""
def websocket_request():
    websocket_url = config["websocket_url"]
    ws = create_connection(websocket_url,
                       sslopt={"cert_reqs": ssl.CERT_NONE},
                       header = [f"Authorization: {generate_auth_header()}"])
    
    return ws
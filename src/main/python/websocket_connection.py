from websocket import create_connection
from utilities import *

"""
    Creates a WebSocket connection.
    
    Note - The credentials (username (client_id) and password (client_secret)) are environment-specific (New Release, Production)

    Args:
        config (json): the json representation of the config file

    Returns:
        WebSocket: The websocket object that can be used to examine market data
"""
def websocket_request(config):
    validate_config(config)
    websocket_url = config["websocket_url"]
    ws = create_connection(websocket_url,
                       header = [f"Authorization: {generate_auth_header(config)}"])
    
    return ws
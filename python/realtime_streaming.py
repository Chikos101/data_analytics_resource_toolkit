import json
from process_data import *
from utilities import *
import time

"""
    Repeatedly updates dataframe using websocket API data

    Args:
        ws (WebSocket): the websocket object from the connection
        config (json): the json representation of the config file
        duration (int): the duration in seconds after which the aggregated messages are returned

    Returns:
        list: the list containing all the received messages from the websocket

"""
def realtime_streaming(ws, config, duration):
    send_subscription_message(ws, config)
    last_print_time = time.time()
    result = []

    while True:
        message = ws.recv()
        data = json.loads(message)
        result.append(data)
        current_time = time.time()
        if current_time - last_print_time >= duration:
            return result
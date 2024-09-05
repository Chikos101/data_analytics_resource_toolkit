from datetime import datetime, timedelta
import time
import json
from process_data import *
from utilities import *

"""
    Repeatedly updates dataframe using websocket API data

    Args:
        ws (WebSocket): the websocket object from the connection
        product_sub (str): the code for the product you want to subscribe to (eg: BTC)
        security_type (str): FUT or OPT

"""
def realtime_streaming(ws, product_sub, security_type):
    # Initialize list of dictionaries
    data_list = {key.split()[1]: {"Month": key.split()[0], "Last": None, "Change": None, "Prior Settle": None, "Open": None, "High": None, "Low": None, "Volume": 0, "Updated": None} for key in get_active_instruments(product_sub,security_type)}
    send_subscription_message(ws, product_sub, security_type)

    while True:
        message = ws.recv()
        data = json.loads(message)
        process_data(data, product_sub, security_type, data_list)
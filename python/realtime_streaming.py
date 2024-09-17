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
def realtime_streaming(ws, config):
    active_globex_symbols = get_active_instruments(config)
    data_list = {key.split()[1]: {"Month": key.split()[0], "Last": None, "Change": None, "Prior Settle": None, "Open": None, "High": None, "Low": None, "Volume": 0, "Updated": None} for key in active_globex_symbols}
    send_subscription_message(ws, config)

    while True:
        message = ws.recv()
        data = json.loads(message)
        print(process_data(data, config, data_list, active_globex_symbols))
from datetime import datetime, timedelta
from utilities import *
from websocket_connection import *
from process_data import *
import time
import json
import pandas as pd

"""
    Repeatedly prints updated quotes table

    Args:
        ws (WebSocket): the websocket object from the connection
        product_sub (str): the code for the product you want to subscribe to (eg: BTC)
        security_type (str): FUT or OPT
        print_interval (int): how often (in seconds) the quotes table should be printed

    Returns:
        json: The json encoded refdata API response
"""
def print_quotes_table(config, duration=20):
    ws = websocket_request(config)
    last_print_time = time.time()
    active_globex_symbols = get_active_instruments(config)
    # Initialize list of dictionaries
    data_list = {key.split()[1]: {"Month": key.split()[0], "Last": None, "Change": None, "Prior Settle": None, "Open": None, "High": None, "Low": None, "Volume": 0, "Updated": None} for key in active_globex_symbols}
    send_subscription_message(ws, config)

    while True:
        message = ws.recv()
        data = json.loads(message)
        process_data(data, config, data_list, active_globex_symbols)
        
        current_time = time.time()
        if current_time - last_print_time >= duration:
            break
    
    print(pd.DataFrame(data_list).T)
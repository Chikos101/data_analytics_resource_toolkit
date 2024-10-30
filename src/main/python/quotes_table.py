from utilities import *
from websocket_connection import *
from process_data import *
import time
import json
import pandas as pd

"""
    Repeatedly updates quotes table and returns as dataframe after the specified duration

    Args:
        config (json): the json representation of the config file
        duration (int): the duration in seconds after which the dataframe  returned

    Returns:
        DataFrame: the dataframe representing the quotes table
"""
def quotes_table(config, duration):
    validate_config(config)
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
    
    return pd.DataFrame(data_list).T
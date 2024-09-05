from datetime import datetime, timedelta
import time
import json
from process_data import *
from utilities import *
import pandas as pd

print_interval = 10 # How often the quotes table should refresh
last_print_time = time.time()

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
def print_quotes_table(ws, product_sub, security_type, print_interval=print_interval):
    # Initialize list of dictionaries
    data_list = {key.split()[1]: {"Month": key.split()[0], "Last": None, "Change": None, "Prior Settle": None, "Open": None, "High": None, "Low": None, "Volume": 0, "Updated": None} for key in get_active_instruments(product_sub, security_type)}
    send_subscription_message(ws, product_sub, security_type)

    while True:
        message = ws.recv()
        data = json.loads(message)
        process_data(data, data_list)
        
        current_time = time.time()
        if current_time - last_print_time >= print_interval:
            print(pd.DataFrame(data_list).T)
            print("---------------------------------------------")
            last_print_time = current_time
from utilities import *
from websocket_connection import *
from refdata_connection import *
from process_data import *
from realtime_streaming import *
from quotes_table import *
from settlements_table import *

import json

config_file = open('config.json')
config = json.load(config_file)

ws = websocket_request(config)
send_subscription_message(ws, config)
print("Start getting active globex symbol")
active_globex_symbols = get_active_instruments(config)
print("Start printing")
print(get_settlements_data(ws,active_globex_symbols))

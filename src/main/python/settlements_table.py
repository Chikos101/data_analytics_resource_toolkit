from datetime import datetime
import json
from process_data import *
from utilities import *
import pandas as pd
import numpy as np


"""
    Processes the data for the settlements table.

    Args:
        data(json): the json representation of the message recieved from websocket

    Returns:
        row(dictionary): the dictionary representation of the data needed to construct a settlements table entry
        --alternatively, none on retrieval failure
"""
def process_settlements_data(data):
    try:
        message_type = data["header"]["messageType"]
        if message_type == "STAT":
            payload = data["payload"][0]
            instrument = payload["instrument"]
            trade_statistics = payload["tradeStatistics"]

            if instrument.get('periodCode', "no Month") == "no Month":
               print("no month", payload)


            row = {
                "Symbol": instrument['symbol'],
                "Month": f"{instrument.get('periodCode', 'no Month')[:4]}-{instrument.get('periodCode', 'no Month')[4:]}",
                "Open": np.nan,
                "High": np.nan,
                "Low": np.nan,
                "Last": np.nan,
                "Change": np.nan,
                "Settle": trade_statistics['settlementPrice'],
                "EST. Volume": np.nan,
                "PRIOR DAY OI": np.nan

            }
            return row
        else:
           return None
    except KeyError:
        pass  # Handle missing keys

    return None



"""
    Subscribe to the settlements data real-time data feed. Outputs the most updated settlements table for in-use products upon completion.

    Args:
        ws(websocket): the websocket that has been subscribed to.
        active_globex_symbols(list[str]): the names of active globex symbols for the requested product(/s).


    Returns:
        quotes_table(DataFrame): the dataframe representation of the requested quotes table.
"""
def get_settlements_data(ws, active_globex_symbols):
  
  active_globex_symbols = [x.split()[1] for x in active_globex_symbols]
   
  current_date = datetime.now()

  initial_quotes_df = pd.DataFrame({
      "Symbol": active_globex_symbols,
      "Month": [f"{current_date.strftime('%Y-%m')}" for i in range(len(active_globex_symbols))],
      "Open": [np.nan for i in range (len(active_globex_symbols))],
      "High": [np.nan for i in range (len(active_globex_symbols))],
      "Low": [np.nan for i in range (len(active_globex_symbols))],
      "Last": [np.nan for i in range (len(active_globex_symbols))],
      "Change": [np.nan for i in range (len(active_globex_symbols))],
      "Settle": [np.nan for i in range (len(active_globex_symbols))],
      "EST. Volume": [np.nan for i in range (len(active_globex_symbols))],
      "PRIOR DAY OI": [np.nan for i in range (len(active_globex_symbols))],
  })

  while True:
    message = ws.recv()
    data = json.loads(message)
    row = process_settlements_data(data)
    number_of_rows_filled = 0

    if row and row['Symbol'] in active_globex_symbols:

        initial_quotes_df.loc[initial_quotes_df['Symbol'] == row['Symbol'], ['Settle']] = row['Settle']
        initial_quotes_df.loc[initial_quotes_df['Symbol'] == row['Symbol'], ['Month']] = row['Month']
        number_of_rows_filled = list(initial_quotes_df['Settle'].isna().values).count(False)

        if number_of_rows_filled == (initial_quotes_df.shape[0]): break

  return initial_quotes_df.drop(columns = {"Open", "High", "Low", "Last", "Change", "EST. Volume", "PRIOR DAY OI"}).reset_index(drop = True).sort_values(by='Month', ascending = True)
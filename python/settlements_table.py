from datetime import datetime, timedelta
import time
import json
from process_data import *
from utilities import *
import pandas as pd
import numpy as np


config_file = open('config.json')
config = json.load(config_file)


def process_data(data):
    try:
        message_type = data["header"]["messageType"]
        if message_type == "TRD":
            payload = data["payload"][0]
            instrument = payload["instrument"]
            trade_summary = payload["tradeSummary"]

            row = {
                "SentTime": data["header"]["sentTime"],
                "UpdateTime": payload["lastUpdateTime"],
                "SeqNumber": data["header"]["sequenceNumber"],
                "ExchangeMic": instrument["exchangeMic"],
                "ProductCode": instrument["productCode"],
                "ProductType": instrument["productType"],
                "Symbol": instrument["symbol"],
                "AggressorSide": trade_summary["aggressorSide"],
                "TradePrice": float(trade_summary["tradePrice"]),
                "TradeQty": int(trade_summary["tradeQty"]),
                "TradeOrderCount": int(trade_summary["tradeOrderCount"]),
                "TradeUpdateAction": trade_summary["tradeUpdateAction"],
                "TradeEntryId": trade_summary["mdTradeEntryId"],
            }
            return row
        elif message_type == "STAT":
            payload = data["payload"][0]
            instrument = payload["instrument"]
            trade_statistics = payload["tradeStatistics"]

            row = {
                "Symbol": instrument['symbol'],
                "Month": f"{trade_statistics['settlementPriceTimestamp'][0:7]}",
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
    except KeyError:
        pass  # Handle missing keys

    return None



"""
Subscribe to the settlements data real-time data feed. Outputs the most updated data as a dataframe upon completion.
"""
def get_settlements_data(ws, active_globex_symbols):
   
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
      row = process_data(data)
      number_of_rows_filled = 0
      
      if row and row['Symbol'] in active_globex_symbols:

        initial_quotes_df.loc[initial_quotes_df['Symbol'] == row['Symbol'], ['Settle']] = row['Settle']


        number_of_rows_filled = list(initial_quotes_df['Settle'].isna().values).count(False)
      
      if number_of_rows_filled == initial_quotes_df.shape[0]: break

  return initial_quotes_df.drop(columns = {"Open", "High", "Low", "Last", "Change", "EST. Volume", "PRIOR DAY OI"})

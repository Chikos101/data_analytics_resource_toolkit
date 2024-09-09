from datetime import datetime, timedelta
import time
import json
from process_data import *
from utilities import *
import pandas as pd
import numpy as np


config_file = open('config.json')
config = json.load(config_file)

def get_active_instruments(ws, access_token):
    products_endpoint = '/products'
    instruments_endpoint = '/instruments'

    def refdata_request(endpoint, headers, params):
        full_url = f'{config.refdata_url}{endpoint}'
        response = requests.get(full_url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f'Error for {endpoint}:', response.status_code, response.text)

    ref_headers = {
        'User-Agent': 'Python',
        "Authorization": f"Bearer {access_token}"
    }

    ref_parameters = {
        "globexProductCode": f"{config.product_sub}",
        "securityType": "FUT"
        }

    refdata_data = refdata_request(products_endpoint, ref_headers, ref_parameters)

    if refdata_data:
        instruments_url = refdata_data["_embedded"]["products"][0]["_links"]["instruments"]["href"]
        instruments_response = requests.get(instruments_url, headers=ref_headers)

        if instruments_response.status_code == 200:
            instruments_data = instruments_response.json()
        else:
            print(f'Error for {instruments_url}:', instruments_response.status_code, instruments_response.text)

    globex_symbols = [
        instrument["globexSymbol"] 
        for instrument 
        in instruments_data["_embedded"]["instruments"]]
    active_globex_symbols = (sorted([symbol for symbol in globex_symbols if not symbol.endswith("XXX") and symbol != "BTCG5"]))
    
    return active_globex_symbols


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

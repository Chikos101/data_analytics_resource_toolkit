from datetime import datetime, timedelta
import pytz
import pandas as pd
from refdata_connection import *

"""
    Filters and processes websocket API data into a dataframe

    Args:
        websocket_data (json): the json representation of data received from the websocket API
        config (json): the json representation of the config file
        dict_result (dict - optional): dictionary to store websocket API data
        active_globex_symbols (list - optional): list of strings containing the active instruments
    
    Returns:
        DataFrame: The dataframe containing the API data

"""
def process_data(websocket_data, config, dict_result=None, active_globex_symbols=None):
    if active_globex_symbols is None:
        active_globex_symbols = get_active_instruments(config)
    
    if dict_result is None:
        dict_result = {key.split()[1]: {"Month": key.split()[0], "Last": None, "Change": None, "Prior Settle": None, "Open": None, "High": None, "Low": None, "Volume": 0, "Updated": None} for key in active_globex_symbols}
    
    try:
        message_type = websocket_data["header"]["messageType"]
        if message_type == "TRD":
            payload = websocket_data["payload"][0]
            instrument = payload["instrument"]
            trade_summary = payload["tradeSummary"]
            UpdateTime = payload["lastUpdateTime"]
            Symbol = instrument["symbol"]
            TradePrice = float(trade_summary["tradePrice"])
            TradeQty = int(trade_summary["tradeQty"])
            Month = instrument["periodCode"]
            key = Month + " " + Symbol

            if key in active_globex_symbols:
                # Parse date and time and convert from UTC to Chicago time
                date_list = UpdateTime.split("T")
                date_str = date_list[0]
                time_str = date_list[1][:8]
                input_datetime = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M:%S")
                utc_time = pytz.utc.localize(input_datetime)

                local_timezone = pytz.timezone("America/Chicago")
                local_time = utc_time.astimezone(local_timezone)

                now = datetime.now(local_timezone)
                time_diff = abs(now - local_time)

                if time_diff < timedelta(minutes=1):
                    if dict_result[Symbol]["Open"] is None:
                        dict_result[Symbol]["Last"] = int(float(TradePrice))
                        dict_result[Symbol]["Open"] = int(float(TradePrice))
                        dict_result[Symbol]["High"] = int(float(TradePrice))
                        dict_result[Symbol]["Low"] = int(float(TradePrice))
                        dict_result[Symbol]["Volume"] = int(TradeQty)
                        dict_result[Symbol]["Change"] = dict_result[Symbol]["Last"] - dict_result[Symbol]["Prior Settle"]
                        dict_result[Symbol]["Updated"] = local_time.strftime("%Y-%m-%d %H:%M:%S")
                    else:
                        dict_result[Symbol]["Last"] = int(float(TradePrice))
                        dict_result[Symbol]["High"] = max(int(float(TradePrice)), dict_result[Symbol]["High"])
                        dict_result[Symbol]["Low"] = min(int(float(TradePrice)), dict_result[Symbol]["Low"])
                        dict_result[Symbol]["Volume"] = int(TradeQty) + dict_result[Symbol]["Volume"]
                        dict_result[Symbol]["Change"] = dict_result[Symbol]["Last"] - dict_result[Symbol]["Prior Settle"]
                        dict_result[Symbol]["Updated"] = local_time.strftime("%Y-%m-%d %H:%M:%S")

        elif message_type == "STAT":
            payload = websocket_data["payload"][0]
            instrument = payload["instrument"]
            trade_stats = payload["tradeStatistics"]
            UpdateTime = payload["lastUpdateTime"]
            key = instrument["periodCode"] + " " + instrument["symbol"]

            if key in active_globex_symbols:
                date_list = UpdateTime.split("T")
                date_str = date_list[0]
                time_str = date_list[1][:8]
                input_datetime = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M:%S")
                utc_time = pytz.utc.localize(input_datetime)

                local_timezone = pytz.timezone("America/Chicago")
                local_time = utc_time.astimezone(local_timezone)

                dict_result[key.split()[1]]["Prior Settle"] = int(float(trade_stats["settlementPrice"]))
                dict_result[key.split()[1]]["Updated"] = local_time.strftime("%Y-%m-%d %H:%M:%S")
        
        return pd.DataFrame(dict_result).T

    except KeyError:
        pass  # Handle missing keys

    return None
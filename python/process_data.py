from datetime import datetime, timedelta
import pytz
import pandas as pd
from refdata_connection import *

"""
    Filters and processes websocket API data into a dataframe

    Args:
        data (json): the json representation of data received from the websocket API
        product_sub (str): the code for the product you want to subscribe to (eg: BTC)
        security_type (str): FUT or OPT
        dict_result (dict): dictionary to store websocket API data
    
    Returns:
        DataFrame: The dataframe containing the API data

"""
def process_data(data, product_sub, security_type, dict_result):
    try:
        message_type = data["header"]["messageType"]
        active_globex_symbols = get_active_instruments(product_sub, security_type)
        if message_type == "TRD":
            payload = data["payload"][0]
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
            payload = data["payload"][0]
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
        
        return pd.DataFrame(dict_result)

    except KeyError:
        pass  # Handle missing keys

    return None
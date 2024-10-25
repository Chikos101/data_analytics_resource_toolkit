from process_data import process_data
from refdata_connection import *
import unittest
import requests
import json
import pandas as pd

config_file = open('config.json')
config = json.load(config_file)


class TestProcessData(unittest.TestCase):
    def test_trade_message(self):
        pass
    def test_stat_message_active_symbols_refdata(self):
        websocket_data = {'header': {'messageType': 'STAT', 
                                     'sentTime': '2024-10-16T00:48:39.731131000Z', 
                                     'sequenceNumber': '3', 'version': '1.0'}, 
                        'payload': [{'lastUpdateTime': '2024-09-26T23:17:05.712524071Z', 
                                     'tradeStatistics': {'settlementActual': True, 
                                                         'settlementFinal': True, 
                                                         'settlementRounded': False, 
                                                         'settlementPrice': '1035.0', # Settle
                                                         'settlementPriceDate': '2024-09-26', 
                                                         'settlementPriceTimestamp': '2024-09-26T23:17:05.712524071Z'}, 
                                                         'instrument': {'definitionSource': 'E', 
                                                                        'exchangeMic': 'XCME', 
                                                                        'id': '42223630', 
                                                                        'marketSeqmentId': '74', 
                                                                        'periodCode': '202409', 
                                                                        'productCode': 'BTC', 
                                                                        'productGroup': 'BF', 
                                                                        'productType': 'FUT', 
                                                                        'symbol': 'BTCU4-BTCX4'}}]}
        active_globex_symbols = get_active_instruments(config)
        # print(active_globex_symbols)
        response = process_data(websocket_data, config, dict_result=None, active_globex_symbols=active_globex_symbols)
        self.assertIsInstance(response, pd.DataFrame)
        self.assertEqual(sorted(response.index), sorted([key.split()[1] for key in active_globex_symbols]))

    def test_stat_message_active_symbols_custom(self):
        websocket_data = {'header': {'messageType': 'STAT', 
                                     'sentTime': '2024-10-16T00:48:39.731131000Z', 
                                     'sequenceNumber': '3', 'version': '1.0'}, 
                        'payload': [{'lastUpdateTime': '2024-09-26T23:17:05.712524071Z', 
                                     'tradeStatistics': {'settlementActual': True, 
                                                         'settlementFinal': True, 
                                                         'settlementRounded': False, 
                                                         'settlementPrice': '1035.0', # Settle
                                                         'settlementPriceDate': '2024-09-26', 
                                                         'settlementPriceTimestamp': '2024-09-26T23:17:05.712524071Z'}, 
                                                         'instrument': {'definitionSource': 'E', 
                                                                        'exchangeMic': 'XCME', 
                                                                        'id': '42223630', 
                                                                        'marketSeqmentId': '74', 
                                                                        'periodCode': '202409', 
                                                                        'productCode': 'BTC', 
                                                                        'productGroup': 'BF', 
                                                                        'productType': 'FUT', 
                                                                        'symbol': 'BTCU4-BTCX4'}}]}  
        active_globex_instruments = ['202410 BTCV4', '202411 BTCX4', '202412 BTCZ4', '202501 BTCF5', '202502 BTCG5', '202503 BTCH5', '202506 BTCM5', '202509 BTCU5']  
        response = process_data(websocket_data, config, dict_result=None, active_globex_symbols=active_globex_instruments)
        self.assertIsInstance(response, pd.DataFrame)
        self.assertEqual(sorted(response.index), sorted([key.split()[1] for key in active_globex_instruments]))

    def test_stat_message_active_symbols_none(self):
        websocket_data = {'header': {'messageType': 'STAT', 
                                     'sentTime': '2024-10-16T00:48:39.731131000Z', 
                                     'sequenceNumber': '3', 'version': '1.0'}, 
                        'payload': [{'lastUpdateTime': '2024-09-26T23:17:05.712524071Z', 
                                     'tradeStatistics': {'settlementActual': True, 
                                                         'settlementFinal': True, 
                                                         'settlementRounded': False, 
                                                         'settlementPrice': '1035.0', # Settle
                                                         'settlementPriceDate': '2024-09-26', 
                                                         'settlementPriceTimestamp': '2024-09-26T23:17:05.712524071Z'}, 
                                                         'instrument': {'definitionSource': 'E', 
                                                                        'exchangeMic': 'XCME', 
                                                                        'id': '42223630', 
                                                                        'marketSeqmentId': '74', 
                                                                        'periodCode': '202409', 
                                                                        'productCode': 'BTC', 
                                                                        'productGroup': 'BF', 
                                                                        'productType': 'FUT', 
                                                                        'symbol': 'BTCU4-BTCX4'}}]}  
        active_globex_symbols = get_active_instruments(config)
        # print(active_globex_symbols)
        response = process_data(websocket_data, config, dict_result=None, active_globex_symbols=None)
        self.assertIsInstance(response, pd.DataFrame)
        self.assertEqual(sorted(response.index), sorted([key.split()[1] for key in active_globex_symbols]))
    
    def test_stat_message_prior_settle(self):
        websocket_data = {'header': {'messageType': 'STAT', 
                                     'sentTime': '2024-10-16T00:48:39.731131000Z', 
                                     'sequenceNumber': '3', 'version': '1.0'}, 
                        'payload': [{'lastUpdateTime': '2024-09-26T23:17:05.712524071Z', 
                                     'tradeStatistics': {'settlementActual': True, 
                                                         'settlementFinal': True, 
                                                         'settlementRounded': False, 
                                                         'settlementPrice': '1035.0', # Settle
                                                         'settlementPriceDate': '2024-09-26', 
                                                         'settlementPriceTimestamp': '2024-09-26T23:17:05.712524071Z'}, 
                                                         'instrument': {'definitionSource': 'E', 
                                                                        'exchangeMic': 'XCME', 
                                                                        'id': '42223630', 
                                                                        'marketSeqmentId': '74', 
                                                                        'periodCode': '202411', 
                                                                        'productCode': 'BTC', 
                                                                        'productGroup': 'BF', 
                                                                        'productType': 'FUT', 
                                                                        'symbol': 'BTCX4'}}]}  
        active_globex_symbols = get_active_instruments(config)
        # print(active_globex_symbols)
        response = process_data(websocket_data, config, dict_result=None, active_globex_symbols=active_globex_symbols)
        self.assertEqual(response.loc['BTCX4']['Prior Settle'], 1035)

        

if __name__ == '__main__':
    unittest.main()


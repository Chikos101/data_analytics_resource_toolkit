from settlements_table import process_settlements_data
import json
import pandas as pd
import sys
import unittest


sys.path.insert(0, '/Users/e46568/dart_poc/src/main/python/')

config_file = open('config.json')
config = json.load(config_file)

class TestProcessSettlementsData(unittest.TestCase):
    def test_trade_message(self):
        pass

    # test for correct settle price for a given instrument
    def test_settle_price(self):
        websocket_data = {'header': 
                          {'messageType': 'STAT', 'sentTime': '2024-10-25T01:47:41.931875000Z', 
                           'sequenceNumber': '3', 'version': '1.0'}, 
                           'payload': [{'lastUpdateTime': '2024-09-26T23:17:05.712524071Z', 
                                        'tradeStatistics': {'settlementActual': True, 
                                                            'settlementFinal': True, 
                                                            'settlementRounded': False, 
                                                            'settlementPrice': '1035.0', 
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
        
        # print(active_globex_symbols)
        response = process_settlements_data(websocket_data)
        self.assertEqual(response['Settle'], 1035)

    # test for correct month for a given instrument
    def test_month(self):
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
        
        # print(active_globex_symbols)
        response = process_settlements_data(websocket_data)
        self.assertEqual(response['Month'], '2024-11')


if __name__ == '__main__':
    unittest.main()
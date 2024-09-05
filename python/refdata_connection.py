import requests
import json
from datetime import datetime
import pandas as pd
from utilities import generate_auth_header

config_file = open('config.json')
config = json.load(config_file)

"""
    Sends request to refdata API and receives a response

    Args:
        endpoint (str): either '/products' or '/instruments'
        product_sub (str): the code for the product you want to subscribe to (eg: BTC)
        security_type (str): FUT or OPT

    Returns:
        json: The json encoded refdata API response
"""
def refdata_request(endpoint, product_sub, security_type):
    ref_headers = {
        'User-Agent': 'Python',
        "Authorization": generate_auth_header()
    }

    ref_parameters = {
        "globexProductCode": f"{product_sub}",
        "securityType": security_type
    }

    refdata_url = config["refdata_url"]
    full_url = f'{refdata_url}{endpoint}'
    response = requests.get(full_url, headers=ref_headers, params=ref_parameters)
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Error for {endpoint}:', response.status_code, response.text)


"""
    Retrieves list of active instruments from reference data

    Args:
        endpoint (str): either '/products' or '/instruments'
        product_sub (str): the code for the product you want to subscribe to (eg: BTC)
        security_type (str): FUT or OPT

    Returns:
        json: The json encoded refdata API response
"""
def get_active_instruments(product_sub, security_type):
    refdata_data = refdata_request('/products',product_sub,security_type)
    ref_headers = {
        'User-Agent': 'Python',
        "Authorization": generate_auth_header()
    }
    if refdata_data:
        instruments_url = refdata_data["_embedded"]["products"][0]["_links"]["instruments"]["href"]
        instruments_response = requests.get(instruments_url, headers=ref_headers)

        if instruments_response.status_code == 200:
            instruments_data = instruments_response.json()
        else:
            print(f'Error for {instruments_url}:', instruments_response.status_code, instruments_response.text)

    globex_symbols = [
        instrument["contractMonth"] + " " + instrument["globexSymbol"] 
        for instrument 
        in instruments_data["_embedded"]["instruments"]
        if datetime.strptime(instrument["firstTradeDate"], '%Y-%m-%d').date() <= pd.to_datetime('today').date()]
    return (sorted([symbol for symbol in globex_symbols if not symbol.endswith("XXX")]))
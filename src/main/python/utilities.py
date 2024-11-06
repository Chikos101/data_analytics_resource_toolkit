import requests
import json

"""
    Generates OAuth header to connect to websocket and refdata APIs

    Args:
        config (json): the json representation of the config file

    Returns:
        str: The OAuth header with the format 'Bearer {Access Token}'
"""
def generate_auth_header(config):
    auth_url = config["auth_url"]
    client_id = config["client_id"]
    client_secret = config["client_secret"]
    auth_response = requests.post(auth_url,
                              data={'grant_type': 'client_credentials'},
                              auth=(client_id, client_secret)
                              )
    access_token = auth_response.json()['access_token']
    return f'Bearer {access_token}'


"""
    Sends websocket TRD and STAT subscription message 

    Note - The credentials (username (client_id) and password (client_secret)) are environment-specific (New Release, Production)

    Args:
        ws (WebSocket): the websocket object from the connection
        config (json): the json representation of the config file

    Returns:
        WebSocket: The websocket object for further processing
"""
def send_subscription_message(ws, config):
    security_type = config["security_type"]
    product_sub = config["product_sub"]
    subscription_message = {
        "header": {
            "messageType": "SUBSCRIBE"
        },
        "payload": {
            "subscriptionMessageTypes": ["STAT", "TRD"],
            "subscriptions": [{
                "productType": security_type,
                "productCode": f"{product_sub}"
            }]
        }
    }

    ws.send(json.dumps(subscription_message))
    return ws


"""
    Validates the config file and raises exceptions if there are invalid parameters

    Args:
        config (json): the json representation of the config file

"""
def validate_config(config):
    keys = ["auth_url", "client_id", "client_secret", "websocket_url", "refdata_url", "product_sub", "security_type"]
    if (not all(key in config for key in keys)):
        raise Exception("Please make sure your config file has the following keys: auth_url, client_id, client_secret, websocket_url, refdata_url, product_sub, security_type")
    
    auth_url = config["auth_url"]
    websocket_url = config["websocket_url"]
    refdata_url = config["refdata_url"]
    security_type = config["security_type"]

    if (not auth_url.startswith("https://auth")):
        raise Exception("Invalid auth url")
    
    if (not websocket_url.startswith("wss://markets")):
        raise Exception("Invalid websocket url")

    if (not refdata_url.startswith("https://refdata")):
        raise Exception("Invalid refdata url")

    if security_type not in ["FUT", "OPT"]:
        raise Exception("Please ensure that the security type is FUT or OPT")
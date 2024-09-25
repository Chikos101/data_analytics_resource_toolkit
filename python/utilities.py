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
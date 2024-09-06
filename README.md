# DART : Data and Analytics Resource Toolkit

# Overview

This repo provides sample code in Python/SQL to help onboard CME Group’s clients with its products and data. Various use cases are discussed for different data sources and types. Check out the [CME Group Product Slate](https://www.cmegroup.com/markets/products.html) for all products.

# Streaming Data

Real-time streaming data related to CME Group products can be accessed via the WebSocket API and Reference Data API.

## Prerequisites

For connecting to the WebSocket API and Reference Data API, an OAuth API ID and a password is required. The API ID must be created and entitled as described here [CME Market Data Over WebSocket API](https://cmegroupclientsite.atlassian.net/wiki/spaces/EPICSANDBOX/pages/46443658/CME+Market+Data+Over+WebSocket+API\#Onboarding-and-Entitlements) & [CMEReferenceDataAPIVersion3](https://cmegroupclientsite.atlassian.net/wiki/spaces/EPICSANDBOX/pages/46114039/CME+Reference+Data+API+Version+3\#CMEReferenceDataAPIVersion3-RestrictedAccess).

**NOTE:** A password is also created during the API ID creation process. Remember to save it at a secure location.

Once, the API ID is created and entitled, add a configuration file with the following parameters:

1. auth\_url \- OAuth authorization server endpoint  
2. client\_id \- API ID  
3. client\_secret \- API password  
4. websocket\_url \- websocket API endpoint  
5. refdata\_url \- refdata API endpoint  
6. product\_sub \- The product code for the product of interest

## Use Cases

### Create Websocket Connection

File location: python/websocket\_connection.py

Description: Creates a connection to the websocket to allow the user to derive real-time data.

Inputs: N/A

Outputs: Returns the Websocket object for further communication / requests

### Send Request to Refdata API

File location: python/refdata\_connection.py

Description: Creates a connection to the reference data API that provides real time access to CME product and instrument referential data

Inputs: endpoint (either products or instruments), product\_sub (the product code), security\_type (either futures or options)

Output: the json object containing the reference data API response

### Get the data in pandas dataframe

File location: python/process\_data.py

Description: Allow the user to query specific data tables depending on their choice of subscription (TRD, STAT, etc) and transform those results to a pandas dataframe.

Inputs: data (json data from the websocket API), product\_sub (the product code), security\_type (either futures or options), dict\_result (dictionary to store the data that should contain the quotes or settlements table headers)

Outputs: N/A

### Stream data in real-time

File location: python/realtime\_streaming.py

Description: Continuously update pandas dataframes with real-time data.

Inputs: ws (the websocket object), product\_sub (the product code), security\_type (either futures or options)

Outputs: a dataframe containing the data from the websocket API

### Quotes Table

File location: python/quotes\_table.py

Description: Recreate the [quotes table](https://www.cmegroup.com/markets/cryptocurrencies/bitcoin/bitcoin.quotes.html) with all active instruments for a product of the user’s choosing.

Inputs: ws (the websocket object), product\_sub (the product code), security\_type (either futures or options), print\_interval (regularity of printing quotes table)

Output: the quotes table is printed at the frequency defined in print\_interval

Example:  
<img src="documents/quotes_table.png" />

### Settlements Table

Description: Get the most recent settlement price for each active Globex symbol for each month for a product of the user’s choosing.  
Inputs: 

Example Output: (DataFrame)  
![][image2]

# Historical Data

Historical data for CME Market Depth can be accessed through a linked dataset subscription to Google Analytics Hub on GCP.

## Prerequisites

Please refer to [Historical Market Depth Data on Google Cloud Platform](https://cmegroupclientsite.atlassian.net/wiki/spaces/EPICSANDBOX/pages/46115012/CME+Historical+Market+Depth+Data+on+Google+Cloud+Platform) to get onboarded with the Google Analytics Hub.

## Use Cases

### Volume-weighted Average Price and Time-weighted Average Price (VWAP/TWAP) Calculations

TWAP Calculations  
File location: SQL/TWAP.sql   
Time weighted average price  
![][image3]  
VWAP Calculations  
File location: SQL/VWAP.sql  
Volume weighted average price  
![][image4]

Inputs: 

* Intervals: desired granularity of calculations returned  
  * String: accepted values \[‘day’, ‘hour’, ‘minute’\]  
* Run\_dates: dates desired to analyze  
  * List of DateTime values  
* Run\_symbols: symbols desired to analyze  
  * List of strings

Output: Bigquery query table of TWAP/VWAP calculations in chronological order  
 ordered by instruments  
Example output: 

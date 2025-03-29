# Install pytz
from fyers_apiv3 import fyersModel # type: ignore
from datetime import datetime, timedelta
from pytz import timezone # type: ignore
import json
import pandas as pd # type: ignore

# Extracting client details
apiCredFile = open('./apiCred.json')
apiCredObject = json.load(apiCredFile)
client_id = apiCredObject['client_id']

# Getting access token
access_tokenFile = open('./access_token.json')
access_tokenObj = json.load(access_tokenFile)
access_token = access_tokenObj['access_token']

fyers = fyersModel.FyersModel(client_id=client_id, token=access_token, is_async=False, log_path="")

symbols = ['RELIANCE', 'HDFCBANK', 'ICICIBANK', 'SBIN', 'INFY', 'HINDUNILVR']
tickers = ['NSE:NIFTY50-INDEX', 'NSE:NIFTYBANK-INDEX']
for symbol in symbols:
    tickers.append("NSE:"+symbol+"-EQ")

ist = timezone('Asia/Kolkata')
current_time = datetime.now(ist)
range_to_date = current_time.strftime('%Y-%m-%d')
range_from_time = current_time - timedelta(days=15)
range_from_date = range_from_time.strftime('%Y-%m-%d')

def spot_inside(data):
    length = len(data)
    timestamps = []
    for i in range(1, length-1):
        if((data[i][2] < data[i-1][2]) and (data[i][3] > data[i-1][3])):
            timestamps.append(datetime.fromtimestamp(data[i][0]).strftime('%d-%m-%Y'))
    return timestamps

filterList = {}
for i in tickers:
    options = {
        "symbol": i,
        "resolution": "D",
        "date_format": "1",
        "range_from": range_from_date,
        "range_to": range_to_date,
        "cont_flag": "1"
    }
    candleData = fyers.history(data=options)['candles']
    inside_bars = spot_inside(candleData)
    filterList[i] = inside_bars
df = pd.DataFrame([(k, ','.join(v) if v else "No inside bars") for k,v in filterList.items()], columns=['Symbol', 'Inside Bar Timestamp'])
print(df)
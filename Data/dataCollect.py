import numpy as np
import pandas as pd
import matplotlib as plt
import time
import io
import requests
import csv
from datetime import datetime, timedelta


# Get Time Range: Currently YTD

now = datetime.now()
ytd = now - timedelta(days=365)


# Subject to change: Currently consists of major world indexes and currencies... and Bitcoin
yahoo_finance_tickers = ['EURUSD=X', 'GBPUSD=X', 'JPY=X', 'USDCNY=X', '^N225', '^GDAXI', '^FTSE', '^DJI', '^GSPC', 'BZ=F', "BTC-USD", 'GC=F']


for tick in yahoo_finance_tickers:
    ticker = tick
    period1 = int(ytd.timestamp())
    period2 = int(now.timestamp())
    interval = '1d' # 1d, 1m

    query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'
    df = pd.read_csv(query_string)
    df['Date'] = pd.to_datetime(df['Date'], format="%Y-%m-%d")
    df['Date'] = df['Date'].dt.strftime("%m/%d/%Y")
    df.to_csv(tick+".csv", index = False)

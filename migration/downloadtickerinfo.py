# Setup environment to pull data from NASDAQ
import pandas as pd
import yfinance as yf
import datetime
import time
import requests
import io

import signal
import sys

def sigint_handler(signal, frame):
    print ('KeyboardInterrupt is caught')
    sys.exit(0)
signal.signal(signal.SIGINT, sigint_handler)

# Setup Boundaries.
# just a few days to testing
# set file storage location
dir =  '/home/pookie/data/historicdata/'

# get all the available tickers
url="https://pkgstore.datahub.io/core/nasdaq-listings/nasdaq-listed_csv/data/7665719fb51081ba0bd834fde71ce822/nasdaq-listed_csv.csv"
s = requests.get(url).content
companies = pd.read_csv(io.StringIO(s.decode('utf-8')))

# make the symbols list
Symbols = companies['Symbol'].tolist()

# create empty dataframe
stock_info = pd.DataFrame()# iterate over each symbol

# Download all the daily data for all symbols for the date range
for symbol in Symbols[:10]:

    # print the symbol which is being downloaded
    try:
        print('Downloading {}'.format(symbol))
        TICK = yf.Ticker(symbol).info

        stock_info = stock_info.append(TICK, ignore_index=True)
        print(stock_info.tail())

    except:
        print('Downloading Error {}'.format(symbol))

# save the data to a file for later use
stock_info.to_csv(dir+'StockInfo.csv')

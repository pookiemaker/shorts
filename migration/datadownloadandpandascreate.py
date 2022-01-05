# Setup environment to pull data from NASDAQ
import pandas as pd
import yfinance as yf
import datetime
import time
import requests
import io

# Setup Boundaries.
# just a few days to testing
start = datetime.datetime(2020,2,1)
end = datetime.datetime(2020,2,11)
# set file storage location
dir =  '/home/pookie/data/historicdata/'

# get all the available tickers
url="https://pkgstore.datahub.io/core/nasdaq-listings/nasdaq-listed_csv/data/7665719fb51081ba0bd834fde71ce822/nasdaq-listed_csv.csv"
s = requests.get(url).content
companies = pd.read_csv(io.StringIO(s.decode('utf-8')))

# make the symbols list
Symbols = companies['Symbol'].tolist()

# create empty dataframe
stock_final = pd.DataFrame()# iterate over each symbol

# Download all the daily data for all symbols for the date range
for i in Symbols:

    # print the symbol which is being downloaded
    print( str(Symbols.index(i)) + str(' : ') + i, sep=',', end=',', flush=True)

    try:
        # download the stock price
        stock = []
        stock = yf.download(i,start=start, end=end, progress=False)

        # append the individual stock prices
        if len(stock) == 0:
            None
        else:
            stock['Name']=i
            stock_final = stock_final.append(stock,sort=False)
    except Exception:
        None

# save the data to a file for later use
stock_final.to_csv(dir+'historicPricing.csv')

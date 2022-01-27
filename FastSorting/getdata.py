
import pandas as pd
import os
import datetime as dt
date_fmt ='%Y%m%d'
import time
import fnmatch
import time
import numpy as np
import yfinance as yf



def writeDataFrame(df,exchange,counter):
    # df is the subgroup data frame that needs written
    # symbol is which one is being written
    # exchange is which exchange it is from_dict
    # Assumption you are running this from a directory as it follows
    # workingdirectory/shortdata/EXCHANGENAME/ExchangeDate.csv
    # workingdirectory/symboldata/data_SYMBOL/EXCHANGENAME_data.csv
    start_time = time.time()
    path = 'stockdata'

    try:
        os.makedirs(path)
    except:
        print('Path already exists')

    filename = path+'/'+exchange+counter+'_data.csv'
    print(filename)
    df.to_csv(filename)
    stop_time = time.time()
    dt = stop_time - start_time
    print('writeSymbol dt = {} '.format(dt))
    return dt

def getSymbolInfo(symbol):
    # need to add a if file exists and has content append, else make new
    try:
        # download the stock price
        TICK = yf.Ticker(symbol).info
        sharesOutstanding = TICK['sharesOutstanding']
        print('=============')
        print('{} Share Outstating: {}'.format(symbol, sharesOutstanding))
    except Exception:
        print(' ::  Problem with yf.Ticker({}).info'.format(symbol))
        return None
    return TICK

def get_ticker_info(Symbols):
    main_df = pd.DataFrame()

    print(main_df.head())
    for symbol in Symbols:
        print('=== new row ===')
        print(symbol)
        derp = getSymbolInfo(symbol)
        if derp != None:
            df = pd.DataFrame.from_dict(derp, orient='index').T
            main_df = pd.concat([main_df,df], ignore_index = True)
    main_df.head()
    return main_df



def get_df(shortdata_dir, exchange, x):
    sdir =  os.path.join(shortdata_dir,exchange)
    prefix = exchange+'shvol'
    # look for files in the date range and make a list
    xxx = []
    for shortdate in x:
        #print(shortdate)
        for file in os.listdir(sdir):
            matchme = prefix+str(shortdate)+'*'
            if fnmatch.fnmatch(file, matchme):
                xxx.append(file)

    # open the files, read them in, and concat them
    dataframes_list =[]
    for file in xxx:
        filename = sdir+'/'+file
        try:
            temp_df = pd.read_csv(filename, delimiter='|',)
            dataframes_list.append(temp_df)

        except:
            print('No file {}'.format(filename))

    df = pd.concat(dataframes_list)
    Symbols = df.Symbol.unique()
    return df, Symbols

def main(start_date, end_date, exchanges, shortdata_dir, graphics =True):

    # generate a date range of interest
    print('=-'*40)
    print(' :: Start Date : \t {} \n :: End Date: \t\t {} '.format(start_date, end_date))
    print('=-'*40)
    x = pd.date_range(start=start_date,end=end_date,freq='D').strftime('%Y%m%d')

    #    shortdata = 'shortdata'
    exchanges   = ['CNMS', 'FNQC', 'FNRA', 'FNSQ', 'FNYX', 'FORF']
    #for exchange in exchanges:
    exchange = exchanges[0]
    df, Symbols = get_df(shortdata_dir, exchange, x)

    counter = 0
    skip = 100
    
    outer = len(Symbols) // skip
    print(outer)
    for jdx in range(outer+1):
        for idx in range(skip):
            print(idx,jdx)
            derp = Symbols[counter:counter+skip]
            counter = counter+1
            derpy = get_ticker_info(derp)
            writeDataFrame(derpy,exchange,str(jdx))
        print(derpy.head())
    return




if __name__ == '__main__':
    # Use these defaults to download EVERYTHING it is about 8GBytes
    # start_date  = '20090101' # Format required -- %Y%m%d
    # end_date    = '20230101' # Format required -- %Y%m%d
    # Initiate the parser
    #parser = argparse.ArgumentParser()
    #parser.add_argument("--ticker", type=str, required=False)
    #args = parser.parse_args()

    #if args.ticker ==None:
    #    symbol ='GME'
    #else:
    #    symbol = args.ticker

    # Test dates to make sure everything is working
    start_date  = '20090101' # Format required -- %Y%m%d
    end_date    = '20220201' # Format required -- %Y%m%d

    exchanges   = ['CNMS', 'FNQC', 'FNRA', 'FNSQ', 'FNYX', 'FORF']

    # FINRA_MARKETS = {
    # 'N': 'FNYX',   # N = NYSE TRF -- Buying
    # 'Q': 'FNSQ',   # Q = NASDAQ TRF Carteret -- Selling
    # 'B': 'FNQC',   # B = NASDAQ TRF Chicago
    # 'D': 'FNRA',   # D = ADF  (almost always 0 data)
    # 'O': 'FORF',   # O = ORF (not actually listed in the spec, but available for download)
    #}

    shortdata_dir ='shortdata'
    parent_dir = 'symboldata'

    main(start_date, end_date, exchanges, shortdata_dir, graphics =True)

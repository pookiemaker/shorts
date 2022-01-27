#
# Purpose is to read in large set of csv downloaded from FINRA, parse into invidual tickers, sort by date and write out into directories.

import pandas as pd
import os
import datetime as dt
date_fmt ='%Y%m%d'
import time
import fnmatch
import time
import numpy as np

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
    for file in xxx[:20]:
        filename = sdir+'/'+file
        try:
            temp_df = pd.read_csv(filename, delimiter='|',,skipfooter=1, engine='python')
            #temp_df = temp_df.dropna()
            temp_df["Date"] = pd.to_datetime(temp_df["Date"], format='%Y%m%d')
            temp_df['NetShort'] =  2*(temp_df.ShortExemptVolume + temp_df.ShortVolume) - temp_df.TotalVolume
            temp_df['NetShortPercent'] = (temp_df.NetShort / temp_df.TotalVolume) * 100
            #temp_df['CumNetShort'] = np.cumsum(temp_df.NetShort)

            dataframes_list.append(temp_df)

        except:
            print('No file {}'.format(filename))

    df = pd.concat(dataframes_list)
    # make dates usable

    # return raw dataframe.

    return df

def writeSymbol(df, symbol, exchange):
    # df is the subgroup data frame that needs written
    # symbol is which one is being written
    # exchange is which exchange it is from_dict
    # Assumption you are running this from a directory as it follows
    # workingdirectory/shortdata/EXCHANGENAME/ExchangeDate.csv
    # workingdirectory/symboldata/data_SYMBOL/EXCHANGENAME_data.csv
    start_time = time.time()
    parent_dir = 'symboldata'
    output_dir  = symbol+'_data' # this can be changed, but this is what I use.

    path = os.path.join(parent_dir, output_dir)
    print('path: {}'.format(path))

    try:
        os.makedirs(path)
    except:
        print('Path already exists')

    filename = path+'/'+exchange+'_data.csv'
    df.to_csv(filename)
    stop_time = time.time()
    dt = stop_time - start_time
    print('writeSymbol dt = {} '.format(dt))
    return dt

def sort_df(df,exchange):
    # get a list of unique symbols
    Symbols = df.Symbol.unique()
    # sort the dataframe by symbol
    gk = df.groupby('Symbol')

    # iterate through all the symbols
    for symbol in Symbols:
        # extract a symbol
        sgk = gk.get_group(symbol)
        # Sort it by date
        sgk = sgk.sort_values(by='Date')

        writeSymbol(sgk, symbol, exchange)
    return

def main(start_date, end_date, exchanges, shortdata_dir, graphics =True):

    # generate a date range of interest
    print('=-'*40)
    print(' :: Start Date : \t {} \n :: End Date: \t\t {} '.format(start_date, end_date))
    print('=-'*40)
    x = pd.date_range(start=start_date,end=end_date,freq='D').strftime('%Y%m%d')

    #    shortdata = 'shortdata'
    exchanges   = ['CNMS', 'FNQC', 'FNRA', 'FNSQ', 'FNYX', 'FORF']
    for exchange in exchanges:
        df = get_df(shortdata_dir, exchange, x)
        sort_df(df, exchange)






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

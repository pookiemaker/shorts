import pandas as pd
import os
import fnmatch
import numpy as np
from matplotlib import pyplot as plt
import datetime as dt
import yfinance as yf
date_fmt ='%Y%m%d'







def getSymbolInfo(path,symbol):
    # need to add a if file exists and has content append, else make new
    try:
        # download the stock price
        TICK = yf.Ticker(symbol).info
        sharesOutstanding = TICK['sharesOutstanding']
        df = pd.DataFrame.from_dict(TICK, orient='index').T
        print(df.head())
        derp = os.path.join(path,symbol+'.csv')
        df.to_csv(derp, mode='w', header = True )
    except Exception:
        print('Error {}'.format(symbol))


    return sharesOutstanding


def calculateNetShorts(df,sharesOutstanding):
    df['NetShort'] = df.TotalVolume - 2*(df.ShortExemptVolume + df.ShortVolume)
    df['NetShortPercent'] = (df.NetShort / df.TotalVolume) * 100
    df['CumNetShort'] = np.cumsum(df.NetShort)
    df['CumNetShortPercentOutstanding']= df.CumNetShort / sharesOutstanding
    df['sharesOutstanding']=sharesOutstanding

    return df

def get_df(sdir, prefix, raw_x, TICKER ):
    '''
    This function iterates through RegSHO data over a data range and pulls rows for a TICKER and
    puts the data into a pandas data frame
    a row is as follows. The consolodated daily short data is in the CNMSyyyymmdd.txt file for every trade day

    Date|Symbol|ShortVolume|ShortExemptVolume|TotalVolume|Market

    '''
    xxx = []
    for shortdate in raw_x:
        #print(shortdate)
        for file in os.listdir(sdir):
            matchme = prefix+str(shortdate)+'*'
            if fnmatch.fnmatch(file, matchme):
                xxx.append(file)

    df = None
    for filename in xxx:

        f = open(sdir+'/'+filename)
        try:
            fullfile = pd.read_csv(f,sep="|")
            if df is None:
                tickerrow = fullfile.loc[fullfile['Symbol'] == TICKER]
                df = tickerrow

            else:
                tickerrow = fullfile.loc[fullfile['Symbol'] == TICKER]
                df = df.append(tickerrow)
        except:
            print('failed: {}'.format(filename))
    return df

def main(start_date, end_date, exchanges, shortdata, symbol, output_dir, path, graphics=False):
    # create date range
    x = pd.date_range(start=start_date,end=end_date,freq='D').strftime('%Y%m%d')

    df_dict ={}
    for exchange in exchanges:
        print(exchange)
        prefix = exchange+'shvol'
        sdir =  os.path.join(shortdata,exchange)
        print(sdir)
        df = get_df(sdir, prefix, x, symbol)
        sharesOutstanding = getSymbolInfo(path,symbol)
        df = calculateNetShorts(df,sharesOutstanding)
        filename = path+'/'+exchange+'_data.csv'
        df.to_csv(filename)
        df_dict[exchange] = df
        if graphics == True:
            raw_x = df['Date']
            df_dt = [dt.datetime.strptime(str(i), date_fmt) for i in raw_x]
            plt.plot(df_dt,df.CumNetShortPercentOutstanding,label=exchange)



    #print(df_dict)
    if graphics == True:
        plt.legend()
        plt.show()


    return


if __name__ == '__main__':
    # Use these defaults to download EVERYTHING it is about 8GBytes
    # start_date  = '20090101' # Format required -- %Y%m%d
    # end_date    = '20230101' # Format required -- %Y%m%d

    symbol ='GME'

    # Test dates to make sure everything is working
    start_date  = '20200101' # Format required -- %Y%m%d
    end_date    = '20200109' # Format required -- %Y%m%d
    #start_date  = '20220101' # Format required -- %Y%m%d
    #end_date    = '20220108' # Format required -- %Y%m%d

    exchanges   = ['CNMS', 'FNQC', 'FNRA', 'FNSQ', 'FNYX', 'FORF']

    # FINRA_MARKETS = {
    # 'N': 'FNYX',   # N = NYSE TRF -- Buying 
    # 'Q': 'FNSQ',   # Q = NASDAQ TRF Carteret -- Selling
    # 'B': 'FNQC',   # B = NASDAQ TRF Chicago
    # 'D': 'FNRA',   # D = ADF  (almost always 0 data)
    # 'O': 'FORF',   # O = ORF (not actually listed in the spec, but available for download)
    #}

    parent_dir = 'symboldata'
    output_dir  = symbol+'_data' # this can be changed, but this is what I use.

    path = os.path.join(parent_dir, output_dir)

    print('path: {}'.format(path))
    try:
        os.makedirs(path)
    except:
        print('Path already exists')

    shortdata = 'shortdata'

    main(start_date, end_date, exchanges, shortdata, symbol, output_dir, path, graphics =True)

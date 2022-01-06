import requests
import pandas as pd
import io
import yfinance as yf
from dictmanip import loader, saver
import os

def main(symboldata, symbol):
    # read the Symbols in

    try:
        # download the stock price
        TICK = yf.Ticker(symbol).info
        sharesOutstanding = TICK['sharesOutstanding']
        df = pd.DataFrame.from_dict(TICK, orient='index').T
        print(df.head())
        derp = os.path.join(path,symbol+'.csv')
        df.to_csv(derp, mode='a', header = True )
    except Exception:
        print('Error {}'.format(symbol))

    print('success')
    return





if __name__ == '__main__':

    symbol = 'GME'
    symboldir = symbol+'_data'
    output_dir = 'symboldata' # this can be changed, but this is what I use.
    path = os.path.join(output_dir, symboldir)
    main(path, symbol)

    '''        try:
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
    '''

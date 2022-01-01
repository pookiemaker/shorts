import requests
import pandas as pd
import io
import yfinance as yf


def main(startindex=0, stopindex=10):
    # read the Symbols in
    symbolbasics = pd.read_csv('SymbolBasics.csv')
    Symbols = symbolbasics['Symbol'].tolist()
    print(Symbols)
    DetailedStockInfo = pd.DataFrame()# iterate over each symbol


    for symbol in Symbols:
        print(symbol)
        try:
            # download the stock price
            TICK = yf.Ticker(symbol).info
            DetailedStockInfo = DetailedStockInfo.append(TICK, ignore_index=True)
            print(DetailedStockInfo.head())
        except Exception:
            print('Error {}'.format(symbol))
        except KeyboardInterrupt:
            print('interrupted!')
            break

    DetailedStockInfo.to_csv('DetailedStockInfo.csv')

    print('success')
    return





if __name__ == '__main__':
    main()

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

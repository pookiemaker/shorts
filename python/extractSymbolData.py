import pandas as pd
import os
import fnmatch

# these two functions came from stack overflow 
def saver(dictex,sdir):
    sdir = sdir+'/'
    for key, val in dictex.items():
        val.to_csv(sdir+"data_{}.csv".format(str(key)))

    with open(sdir+"keys.txt", "w") as f: #saving keys to file
        f.write(str(list(dictex.keys())))

def loader(sdir):
    """Reading data from keys"""
    with open(sdir+"keys.txt", "r") as f:
        keys = eval(f.read())

    dictex = {}
    for key in keys:
        dictex[key] = pd.read_csv(sdir+"data_{}.csv".format(str(key)))

    return dictex


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

def main(start_date, end_date, exchanges, shortdata, symbol, output_dir, path):
    # create date range
    x = pd.date_range(start=start_date,end=end_date,freq='D').strftime('%Y%m%d')

    df_dict ={}
    for exchange in exchanges:
        print(exchange)
        prefix = exchange+'shvol'
        sdir =  os.path.join(shortdata,exchange)
        df = get_df(sdir, prefix, x, symbol)
        df_dict[exchange] = df

    #print(df_dict)
    saver(df_dict,path)
    return


if __name__ == '__main__':
    # Use these defaults to download EVERYTHING it is about 8GBytes
    # start_date  = '20090101' # Format required -- %Y%m%d
    # end_date    = '20230101' # Format required -- %Y%m%d

    symbol ='GME'

    # Test dates to make sure everything is working
    start_date  = '20200101' # Format required -- %Y%m%d
    end_date    = '20200109' # Format required -- %Y%m%d

    exchanges   = ['CNMS', 'FNQC', 'FNRA', 'FNSQ', 'FNYX']

    parent_dir = 'symboldata'
    output_dir  = symbol+'_data' # this can be changed, but this is what I use.

    path = os.path.join(parent_dir, output_dir)

    print('path: {}'.format(path))
    try:
        os.makedirs(path)
    except:
        print('Path already exists')

    shortdata = 'shortdata'

    main(start_date, end_date, exchanges, shortdata, symbol, output_dir, path)

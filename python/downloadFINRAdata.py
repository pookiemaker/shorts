# Function to download FINRA data


# Im sure there is a better / more correct way to do this.

import pandas as pd
import requests
import os

def main(start_date, end_date, exchanges, sdir):
    # Using the start and end dates generate a pandas dataframe with
    # all the dates.
    x = pd.date_range(start=start_date,end=end_date,freq='D').strftime('%Y%m%d')
    output_dir = './'+sdir+'/' # format it up for writing to the correct Place
    postfix = '.txt'

    base_url = 'https://cdn.finra.org/equity/regsho/daily/'
    for exchange in exchanges:
        exchange_dir = output_dir +exchange+'/'
        print(exchange_dir)
        for idx in range(len(x)):
            url = ""
            pulldate = x[idx] # get the date to pull
            filename = exchange+'shvol'+pulldate+postfix
                # CNMSshbvol20190101.txt
            url = base_url + filename
            print(filename)
            r = requests.get(url)

            if r.status_code != 200:
                print('\t :: Error reading {}'.format(filename))
            else:
                s = requests.get(url).content
                f=open(exchange_dir+filename,'wb')
                f.write(s)
                f.close
    return

if __name__ == '__main__':
    # make the output Directory manually.
    #  it just overwrites what is there.
    exchanges   = ['CNMS', 'FNQC', 'FNRA', 'FNSQ', 'FNYX']
    try:
        output_dir = 'shortdata' # this can be changed, but this is what I use.
        for exchange in exchanges:
            parent_dir = output_dir
            path = os.path.join(parent_dir, exchange)
            os.makedirs(path)
    except:
        print('Directorys exist')

    # Use these defaults to download EVERYTHING it is about 8GBytes
    # start_date  = '20090101' # Format required -- %Y%m%d
    # end_date    = '20230101' # Format required -- %Y%m%d

    # Test dates to make sure everything is working
    start_date  = '20200101' # Format required -- %Y%m%d
    end_date    = '20200109' # Format required -- %Y%m%d

    success = main(start_date, end_date, exchanges, output_dir )

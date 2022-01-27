import pandas as pd
import os
import extractSymbolData as esd

filename = '/home/pookie/git/shorts/shortvolume/shortdata/FNSQ/FNSQshvol20090803.txt'



# Use these defaults to download EVERYTHING it is about 8GBytes
start_date  = '20090101' # Format required -- %Y%m%d
end_date    = '20230101' # Format required -- %Y%m%d


symbol ='GME'


# Test dates to make sure everything is working
#start_date  = '20200101' # Format required -- %Y%m%d
#end_date    = '20200109' # Format required -- %Y%m%d
#start_date  = '20211201' # Format required -- %Y%m%d
#end_date    = '20220130' # Format required -- %Y%m%d

exchanges   = ['CNMS', 'FNQC', 'FNRA', 'FNSQ', 'FNYX', 'FORF']


shortdata = 'shortdata'

f = open(filename)
df = pd.read_csv(f,sep="|")

derp = df['Symbol']
start = 156
idx = start
for symbol in derp[start:]:
    idx = idx+1 
    parent_dir = 'symboldata'
    output_dir  = symbol+'_data' # this can be changed, but this is what I use.
    path = os.path.join(parent_dir, output_dir)
    print('=-'*40)
    print('path: {}'.format(path))
    print(' Index \# {}'.format(idx))
    print('=-'*40)
    try:
        os.makedirs(path)
    except:
        print('Path already exists')
    #print(symbol)
    esd.main(start_date, end_date, exchanges, shortdata, symbol, output_dir, path, graphics =False)

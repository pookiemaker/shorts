# This simple script grabs all the DAILY data from RegSHO at FINRA Adjust the dates as required.
# It default pulls the combined data set CNMS...

import pandas as pd
import requests

# Generate dates to pull logs with
x = pd.date_range(start='20211101',end='20220101',freq='D').strftime('%Y%m%d')

#https://cdn.finra.org/equity/regsho/daily/CNMSshvol20211206.txt
burl = 'https://cdn.finra.org/equity/regsho/daily/'
#dir = 'shortdata2/'
dir =  '/home/pookie/data/shortdata2/'

prefix = 'CNMSshvol' # NMS
#prefix = 'FNQCshvol' # NMS
#prefix = 'FNRAshvol' # NMS
#prefix = 'FNSQshvol' # NMS
#prefix = 'FNYXshvol' # NMS

postfix = '.txt'
for idx in range(len(x)):
    url =""
    pull = x[idx]
    filename = prefix+pull+postfix
    url =burl+filename
    print(filename, burl)
    r = requests.get(url)

    if r.status_code == 404:
        print('404 Error')
    else:
        s = requests.get(url).content
        f=open(dir+filename,'wb')
        f.write(s)
        f.close

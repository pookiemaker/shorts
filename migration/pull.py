# This simple script grabs all the DAILY data from RegSHO at FINRA Adjust the dates as required.
# It default pulls the combined data set CNMS...

import pandas as pd
import requests

# Generate dates to pull logs with
x = pd.date_range(start='20200601',end='20210801',freq='D').strftime('%Y%m%d')


burl = 'http://regsho.finra.org/'
#dir = 'shortdata2/'
dir =  '/mnt/5c823cd2-502b-4990-a220-579838be1f10/data/shortdata2/'

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
    print(burl)
    r = requests.get(url)

    if r.status_code == 404:
        print('404 Error')
    else:
        s = requests.get(url).content
        f=open(dir+filename,'wb')
        f.write(s)
        f.close

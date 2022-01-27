import pandas as pd
import os
import datetime as dt
date_fmt ='%Y%m%d'
import time

def getListOfFiles(dirName):
    # create a list of file and sub directories
    # names in the given directory
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)

    return allFiles

path ='shortdata'
exch ='CNMS'
findme = os.path.join(path,exch)
derp = getListOfFiles(findme)

# create empty list
dataframes_list = []


for file in derp:
    working = open(file,'r')
    temp_df = pd.read_csv(file, delimiter='|',)
    temp_df = temp_df.dropna()
    dataframes_list.append(temp_df)
df = pd.concat(dataframes_list)
df["Date"] = pd.to_datetime(df["Date"], format='%Y%m%d')
Symbols = df.Symbol.unique()
Symbols

gk = df.groupby('Symbol')


starttime = time.time()
list_time = []
list_df = []
counter = 0
for symbol in Symbols:
    counter += 1
    sgk = gk.get_group(symbol)
    sgk = sgk.sort_values(by='Date')

    list_time.append(time.time()-starttime)
    #df = df.drop(df[df['Symbol'] == symbol].index)



sgk.head()

from matplotlib import pyplot as plt
import numpy as np
np_time = np.array(list_time)
plt.plot(np_time[:-2]-np_time[2:])
plt.show()

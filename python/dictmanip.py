
#https://www.titanwolf.org/Network/q/c1712969-f271-4eff-b6f2-07ae14917d1b/y


import csv
import pandas as pd

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

#(...)

#dictex = loader()

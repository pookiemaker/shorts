# these two functions came from stack overflow
def saver(dictex,sdir):
    sdir = sdir+'/'
    for key, val in dictex.items():
        val.to_csv(sdir+"data_{}.csv".format(str(key)))

    with open(sdir+"keys.txt", "w") as f: #saving keys to file
        f.write(str(list(dictex.keys())))
    return

def loader(sdir):
    """Reading data from keys"""
    with open(sdir+"keys.txt", "r") as f:
        keys = eval(f.read())

    dictex = {}
    for key in keys:
        dictex[key] = pd.read_csv(sdir+"data_{}.csv".format(str(key)))

    return dictex

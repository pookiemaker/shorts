# Short Volume study

This repository explores the stock market. I noticed a disagreement between the short volume, and reported short interest in a particular idiosyncratic stock. I decided to explore GME. I noticed the reported short interest is about 2 orders of magnitude off of what the short volume of daily was reported. So I decided to to all the entries of the stock market with available free data.

The data you need
* All available TICKERS  (yfinance)
* Daily Short Volume (FINRA)
* Short Exempt Volume (FINRA)
* Total Volume (FINRA)
* Total Outstanding shares for each firm (yfinance)
* Historical Pricing for each ticker (yfinance)

# Methodology

## Get overall TICKER awareness

We start with `python getSymbols.py` to download a list of available tickers with very basic information from yahoo finance into `SymbolBasics.csv`.
`index, Symbol,Company Name,Security Name,Market Category,Test Issue,Financial Status,Round Lot Size`

## Glean individual TICKER awareness

Next we use `python getTickerInfo.py` to get detailed data for each stock. We ask yfinance with `currentTicker = yf.Ticker(TICKER).info` for the detailed info about every stock. Right now we are only using the `sharesOutstating` entry. We associate the total shares outstanding/issued with each individual TICKER. This is used for calculations

## Download historical price data
This takes ALOT of space. `FIXME: Build this all tickers` This is needed for weighting and figuring out how much the shorts have.

## Download The ShortVolume data and store it.
The URL location at FINRA seems to float around a bit -- you may have to figure that out. The default timeline built into `python pullFINRAshortVolume_cdn.py` is from Jan 2018 to Jan 2022. The data downloads the consolidated reports on a daily basis. Each day is a separate file and is default saved into `./shortdata`. As the data is being downloaded you will see `filenames` and `error` values streaming by. The `error`s are for days the markets are closed.

# Process

1. Load ShortVolume data into a pandas data DataFrame `big_df`
    1. Remove NaN entires
1. Load Symbols(TICKERS) into a pandas DataFrame
1. Load and extract each symbol(TICKER) data with 'outstandingShares'
1. Calculate 'NetShort' for all entries in `big_df`
    $$NetShort = TotalVolume - 2*(ShortExemptVolume + ShortVolume)$$
1. Iterate through each symbol(TICKER)
    1. Calculate raw Cumulative NetShort Position
        `symbol_df['CumNetShort']=np.cumsum(symbol_df['NetShort']) )`
    1. Calculate NetShort Percentage Position
        `symbol_df['NetShortPercent']=symbol_df['CumNetShort'])/sharesOutstating`
    1. <optional> add historical pricing to calculate short obligation
    1. Add to new `sorted_big_df`



## Load individual ticker awareness


## Load the a

Now

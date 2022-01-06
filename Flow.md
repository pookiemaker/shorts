# Overall Flow for collecting and processing datahub

1. Download the RegSHO data for the time in question using `%Y%m%d` format `20200102`. That is 2020, Jan, 02
  `downloadFINRAdata.py`
  Puts data in `./shortdata/exchange/...`

1. PreProcess RegSHO daily data for a particular stock symbol
  `extractSymbolData.py`
  Puts data in `./symboldata/{symbol}_data/...`

1. Process the Symbols Specific RegSHO data
  Load the processed file in.
  

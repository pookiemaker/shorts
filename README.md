# Dealing with RegSHO DAILY Data
To work with RegSHO data you need to download the data locally and then parse it. 

```pull.py``` is a python script that will pull down data from FINRA. You will need about 500M of space to download it. It starts from the first date and runs through. It skips dates withouth data via 404 error handling. 

# Analysing the Data 
is in ShortAnalysis.ipynb 
This is an ipython notebook. It will work for any TICKER. GME is the example 

# Where to get the data

* https://www.sec.gov/data/foiadocsfailsdatahtm -- zip files for b-monthly FTDs aggregated 
* https://www.sec.gov/opa/data/market-structure/marketstructuredownloadshtml-by_security.html -- viziabliity into trades/cancels etc 





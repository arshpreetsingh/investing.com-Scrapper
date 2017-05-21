## Synopsis

using python to fetch data from investing.com and plotting web-based using Bookeh 

## How to run(from ubuntu terminal)

#action=historical_data&curr_id=1&st_date=04%2F21%2F2016&end_date=05%2F21%2F2017&interval_sec=Daily

#request URL

https://www.investing.com/instruments/HistoricalDataAjax

data:

action:historical_data
curr_id:1
st_date:04/21/2016
end_date:05/21/2017
interval_sec:Monthly

```
$ python scrapper.py
```
Above command will fetch data and create DB(mydb) file in your current dictionary.  

```
$ python scrapper.py
```
Above command will disply plot in your browser

## Installation(using conda)
```
conda install sqlalchemy
conda install numpy
conda install pandas
conda install urllib2
conda install -c anaconda beautifulsoup4=4.6.0
```

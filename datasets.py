from classes.hashmap import *
from datetime import datetime
# write in terminal pip install yfinance
import yfinance as yf
import pandas as pd


url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
sp500_table = pd.read_html(url)
sp500_tickers = sp500_table[0]['Symbol'].tolist()
stocks_size = len(sp500_tickers)

data = yf.download(sp500_tickers, start='2022-01-01', end='2022-01-31', group_by='ticker')
stocks_list = HashMap(stocks_size)

for i in sp500_tickers:
    data_stock = data[i]
    size = len(data_stock)
    stock = HashMap(size)
    for i,k in enumerate(data_stock.index):
        value = []
        date_string = str(k)
        parsed_date = datetime.fromisoformat(date_string)
        cleaned_date = parsed_date.strftime('%Y-%m-%d')
        for j in data_stock.iloc[i]:
            value.append(j)

        stock.put(cleaned_date,value)

    stocks_list.put(i,stock)

print(stocks_list.get("AAPL"))



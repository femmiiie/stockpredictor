#stl imports
import csv

#external library imports
import yfinance as yf
import pandas as pd
from dearpygui.dearpygui import set_value

#project imports
from classes.hashmap import *
from globals import *


def download_data():

  url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
  sp500_table = pd.read_html(url)
  sp500_tickers = sp500_table[0]['Symbol'].tolist()
  

  data : pd.DataFrame = yf.download(sp500_tickers, period="max", group_by='ticker')
  # data = yf.download(sp500_tickers, start='2022-01-01', end='2022-01-31', group_by='ticker')

  failed = [stock for stock in sp500_tickers if stock not in data.columns.levels[0]]

  total_stocks = len(sp500_tickers) - len(failed)

  with open("stock_info.csv", "x", newline='') as file:
    writer = csv.writer(file, delimiter="|")

    for i, stock in enumerate(sp500_tickers, start=1):
      row_count = sum(1 for _, row in data[stock].iterrows() if not pd.isna(row.iloc[0]))

      if stock in failed or row_count == 0: #prevents stocks with no data getting written
        continue

      writer.writerow([stock, row_count])

      for _, row in data[stock].iterrows():
        if pd.isna(row.iloc[0]): #skip row if no data for date exists
          continue

        list = [str(row.name)[:9]]
        list.extend(row)

        writer.writerow(list)

      set_value(progress_bar, i/total_stocks) #updates progress bar
      # print(f"{stock} writing finished")


def get_stock_list():
  name_list = []
  count = 0

  with open("stock_info.csv", mode="r") as file:
    reader = csv.reader(file, delimiter='|')
    for line in reader:

      if (len(line)) == 2:
        name_list.append(line[0])
        count += 1
        set_value(progress_bar, count/503)
      
  return name_list


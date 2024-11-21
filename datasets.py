#stl imports
import csv
import asyncio

#external library imports
import yfinance as yf
import pandas as pd
from dearpygui.dearpygui import set_value

#project imports
from classes.hashmap import *
from globals import *


def download_data():

  #edit if you want to pull custom data, we use the full list of current S&P 500 companies
  url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
  sp500_tickers = pd.read_html(url)[0]['Symbol'].tolist()
  data : pd.DataFrame = yf.download(sp500_tickers, period="max", group_by='ticker')
  failed = [stock for stock in sp500_tickers if stock not in data.columns.levels[0]]

  total_stocks = len(sp500_tickers) - len(failed)

  with open("stock_info.csv", "x", newline="") as file:
    writer = csv.writer(file, delimiter="|")

    for i, stock in enumerate(sp500_tickers, start=1):
      row_count = sum(1 for _, row in data[stock].iterrows() if not pd.isna(row.iloc[0]))

      if stock in failed or row_count == 0: #prevents stocks with no data getting written
        continue

      writer.writerow([stock, row_count])

      for _, row in data[stock].iterrows():
        if pd.isna(row.iloc[0]): #skip row if no data for date exists
          continue

        list = [str(row.name)[:9]] #format datetime to only have the date
        list.extend(row)

        writer.writerow(list)

      set_value(progress_bar, i/total_stocks) #updates progress bar


def get_stock_list():
  name_list = []
  count = 0

  with open("stock_info.csv", mode="r") as file:
    reader = csv.reader(file, delimiter="|")
    for line in reader:

      if (len(line)) == 2:
        name_list.append(line[0])
        count += 1
        set_value(progress_bar, count/503)
      
  return name_list


async def pull_stock_info(stock_name : str):
  
  if not stock_name:
    return

  stock_name = stock_name.upper()
  print("pulling data")

  async with data_lock: #prevents other code from using the hashmap while updating
    with open("stock_info.csv", mode="r") as file:
      reader = csv.reader(file, delimiter="|")
      line_count = 0

      #iterate until we are at the requested stock
      for line in reader:
        if line[0] == stock_name:
          line_count = line[1]
          break
      
      if line_count == 0:
        return

      current_stock_data = HashMap(int(int(line_count)/0.7))

      for line in reader:
        if len(line) == 2: #check if we are done
          break

        current_stock_data.put(line[0], line[1:-1])

  print("done pulling data")

  #to-do: add callbacks so visualizer can update data
#stl imports
import csv
import asyncio
from os import path

#external library imports
import yfinance as yf
import pandas as pd
from dearpygui.dearpygui import set_value


#project imports
import data.globals as globals


def download_data():
  if path.exists("stock_info.csv"):
    return

  #edit if you want to pull custom data, we use the full list of current S&P 500 companies
  url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
  sp500_tickers = pd.read_html(url)[0]['Symbol'].tolist()
  data : pd.DataFrame = yf.download(sp500_tickers, start="2010-01-01", end="2024-11-7", group_by='ticker', rounding=True)
  failed = [stock for stock in sp500_tickers if stock not in data.columns.levels[0]]

  total_stocks = len(sp500_tickers) - len(failed)

  with open("stock_info.csv", "x", newline="") as file:
    writer = csv.writer(file, delimiter="|")

    for i, stock in enumerate(sp500_tickers, start=1):
      row_count = sum(1 for _, row in data[stock].iterrows() if not (pd.isna(row.iloc[0]) or row.iloc[0] == 0.0))

      if stock in failed or row_count == 0: #prevents stocks with no data getting written
        continue

      writer.writerow([stock, row_count])

      for _, row in data[stock].iterrows():
        if pd.isna(row.iloc[0]) or row.iloc[0] == 0.0: #skip row if no data for date exists
          continue

        list = [str(row.name)[:10]] #format datetime to only have the date
        list.extend(row)

        writer.writerow(list)

      set_value(globals.progress_bar, i/total_stocks) #updates progress bar


def get_stock_list():
  name_list = []
  count = 0

  with open("stock_info.csv", mode="r") as file:
    reader = csv.reader(file, delimiter="|")
    for line in reader:

      if (len(line)) == 2:
        name_list.append(line[0])
        count += 1
        # print(f"Adding stock: {line[0]} (Count: {count})")
        set_value(globals.progress_bar, count/503)
      
  return name_list


async def pull_stock_info(stock_name : str):
  
  if not stock_name:
    print("stk data no found")
    return

  stock_name = stock_name.upper()

  async with globals.data_lock: #prevents other code from using the hashmap while updating
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

      globals.current_stock_data = None
      globals.current_stock_data = {}

      for line in reader:
        if len(line) == 2: #check if we are done
          break
        globals.current_stock_data[line[0]] = [float(i) for i in line[1:]]


#variant of pull stock info that yields all stock maps iteratively
def stock_info_iter():
  with open("stock_info.csv", mode="r") as file:
    reader = csv.reader(file, delimiter="|")
    data = None
    curr_stock = ""

    for line in reader:
      if reader.line_num == 1:
        curr_stock = line[0]
        data = {}

      elif len(line) == 2:
        yield curr_stock, data

        curr_stock = line[0]
        data = {}

      else:
        data[line[0]] = [float(i) for i in line[1:]]
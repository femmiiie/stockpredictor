#stl imports
import csv
import asyncio

#external library imports
import yfinance as yf
import pandas as pd
from dearpygui.dearpygui import set_value
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plt
from datetime import timedelta, datetime

#project imports
from classes.hashmap import *
import globals


def download_data():

  #edit if you want to pull custom data, we use the full list of current S&P 500 companies
  url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
  sp500_tickers = pd.read_html(url)[0]['Symbol'].tolist()
  data : pd.DataFrame = yf.download(sp500_tickers, period="max", group_by='ticker', rounding=True)
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
      globals.current_stock_data = HashMap(int(int(line_count)/0.7))

      for line in reader:
        if len(line) == 2: #check if we are done
          break
        globals.current_stock_data[line[0]] = [float(i) for i in line[1:-1]]

def train_model(stock_data: HashMap):
   extracted_data = {key: value for key, value in stock_data.items()}
   columns = ["Close", "Open", "High", "Low", "Volume"]
   try:
     df = pd.DataFrame.from_dict(extracted_data, orient="index", columns=columns)
   except ValueError as e:
     print("err creating df")
     raise
   
   df.index = pd.to_datetime(df.index)
   df.sort_index(inplace=True)

   df["Tomorrow"] = df["Close"].shift(-1) 
   df = df.dropna() 

   predictors = ["Close", "Volume", "Open", "High", "Low"]

   train = df.iloc[:-100]
   test = df.iloc[-100:]

   model = RandomForestRegressor(n_estimators=200, random_state=1)
   model.fit(train[predictors], train["Tomorrow"])

   current_date = pd.Timestamp(datetime.now()) 
   start_date = max(df.index[-1], current_date)
   future_dates = pd.date_range(start=start_date + timedelta(days=1), periods=30)  # 30 days

   future_df = pd.DataFrame(index=future_dates)
   future_df["Close"] = None

   # "Predict future prices"
   last_row = df.iloc[-1][["Close", "Volume", "Open", "High", "Low"]].to_frame().T
   for i in range(len(future_df)):
        predicted_close = model.predict(last_row)[0]

        if i > 0:
            predicted_close = max(predicted_close, future_df.iloc[i - 1]["Close"] * 0.95)  
            predicted_close = min(predicted_close, future_df.iloc[i - 1]["Close"] * 1.05)  

        future_df.iloc[i, future_df.columns.get_loc("Close")] = predicted_close

        last_row = pd.DataFrame([[
            predicted_close,
            last_row.iloc[0]["Volume"] * np.random.uniform(0.98, 1.02),  
            predicted_close * np.random.uniform(0.99, 1.01),           
            predicted_close * np.random.uniform(1.00, 1.02),           
            predicted_close * np.random.uniform(0.98, 1.00),            
        ]], columns=predictors)

    # Plot with future predictions
   plt.figure(figsize=(10, 6))
   plt.plot(future_df.index, future_df["Close"], label="Predicted Prices", color="orange")
   plt.title("Predicted Future Stock Prices (Next 30 Days)")
   plt.xlabel("Date")
   plt.ylabel("Price")
   plt.legend()
   plt.grid()
   plt.show()
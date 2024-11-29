#stl imports
import asyncio
from datetime import datetime, timedelta
from os import path
from time import sleep

#external library imports
import dearpygui.dearpygui as gui

#project imports
from classes.hashmap import *
from classes.trie import *
from data.datasets import *
import data.globals as globals


def filter_options(stocks : Trie):
  input_text : str = gui.get_value("search").upper()
  filtered_items = [item for item in sorted(stocks.get_searched_list(input_text)) if input_text in item]
  gui.configure_item("dropdown", items=filtered_items)


def show_listbox():
  gui.show_item("dropdown")


def hide_listbox():
  sleep(0.1)
  gui.hide_item("dropdown")


def select_item(sender):
  text = gui.get_value(sender)
  gui.set_value("search", text)
  pull_wrapper()


def pull_wrapper():
  async def pull():
    await pull_stock_info(gui.get_value("search"))
    await update_graph()

  sleep(0.1)
  asyncio.run(pull())

async def update_graph():
  dates = []
  opens = []
  highs = []
  lows = []
  closes = [] #define all lists that gui needs to render candlestick graph

  async with globals.data_lock:
    for date in sorted(globals.current_stock_data.keys()):
      vals = globals.current_stock_data[date]

      dates.append(date)
      opens.append(vals[0])
      highs.append(vals[1])
      lows.append(vals[2])
      closes.append(vals[3])

  #approx num of business days in 10 years
  time_range = 2500

  # print([(value, index) for index, value in enumerate(dates) if index % 1500 == 0])
  # print([i + len(dates) - time_range for i in range(time_range)])

  
  #reformat ticks to match available stock data for ticker
  if len(dates) < time_range:
    time_range = len(dates)
  
  gui.set_axis_ticks("x-axis", ((dates[-time_range], len(dates) - time_range), (dates[int(-time_range/2)], len(dates) - int(time_range/2)), (dates[-1], len(dates) - 1)))

  gui.delete_item("candlestick")
  gui.add_candle_series(
    [i + len(dates) - time_range for i in range(time_range)],
    opens[-time_range:-1],
    closes[-time_range:-1],
    lows[-time_range:-1],
    highs[-time_range:-1],
    tag="candlestick",
    parent="y-axis"
  )


def update_date_range():
    start_val = gui.get_value("start_date")
    end_val = gui.get_value("end_date")
    date_format = "%m/%d/%Y"

    start_date = datetime.strptime(start_val, date_format)
    end_date = datetime.strptime(end_val, date_format)

    if start_date > end_date:
      gui.set_value("start_date", end_date.strftime(date_format))
      gui.set_value("end_date", start_date.strftime(date_format))


def reset_loading_screen():
  gui.set_value(globals.progress_bar, 0)


#very basic state logic since the app only has 3 screens to deal with
def swap_visible_screen(swap_to : int):

  if swap_to == 1:
    gui.show_item("Primary")
    gui.set_primary_window("Primary", True)
    gui.hide_item("Credits")
    gui.hide_item("Predictor")
    gui.hide_item("Loading")

  elif swap_to == 2:
    gui.hide_item("Primary")
    gui.show_item("Credits")
    gui.set_primary_window("Credits", True)
    gui.hide_item("Predictor")

  elif swap_to == 3:
    gui.hide_item("Primary")
    gui.hide_item("Credits")
    gui.show_item("Predictor")
    gui.set_primary_window("Predictor", True)


def set_defaults(first_item):
  gui.set_value("search", first_item)
  pull_wrapper()
  

import matplotlib.pyplot as plt
import numpy as np
import joblib
from sklearn.preprocessing import OneHotEncoder
import pandas as pd

def predict():
  stock = gui.get_value("search")
  data = yf.download(stock, period="1mo", group_by="ticker", rounding=True) #get last month of stock activity to seed model

  columns = None
  feature_columns = None
  with open("cols.conf", "r", newline="") as file:
    reader = csv.reader(file, delimiter="|")
    it = iter(reader)
    columns = next(it)
    feature_columns = next(it)


  formatted = []
  for _, row in data[stock].iterrows():
    if not pd.isna(row.iloc[0]) and row.iloc[0] != 0.0:
      formatted.append([str(row.name)[:10]] + row.to_list())

  recent_data = pd.DataFrame.from_dict({line[0]: [float(i) for i in line[1:]] for line in formatted}, orient="index", columns=columns)
  recent_data.index = pd.to_datetime(recent_data.index)
  recent_data.sort_index(inplace=True)
  recent_data["Stock_ID"] = stock

  for lag in range(1, 6):
    recent_data[f"Close_lag_{lag}"] = recent_data["Close"].shift(lag)
  recent_data = recent_data.dropna()

  model = joblib.load("stock_model.pkl")

  start_date = pd.Timestamp(gui.get_value("start_date"))
  end_date = pd.Timestamp(gui.get_value("end_date"))
  future_df = pd.DataFrame(index=pd.date_range(start_date, end_date))
  future_df["Close"] = None

  encoder = OneHotEncoder(sparse_output=False)
  stock_id = encoder.fit_transform(recent_data[["Stock_ID"]])
  stock_df = pd.DataFrame(stock_id, index=recent_data.index, columns=encoder.get_feature_names_out(["Stock_ID"]))

  recent_data = pd.concat([recent_data, stock_df], axis=1)

  # "Predict future prices"
  last_row = recent_data.iloc[-1][feature_columns].to_frame().T
  for i in range(len(future_df)):
    predicted_close = model.predict(last_row)[0]

    if i > 0:
      historical_volatility = recent_data["Close"].pct_change().std()
      predicted_close = max(predicted_close, future_df.iloc[i - 1]["Close"] * (1-historical_volatility))
      predicted_close = min(predicted_close, future_df.iloc[i - 1]["Close"] * (1+historical_volatility))

    future_df.iloc[i, future_df.columns.get_loc("Close")] = predicted_close

    last_row = pd.DataFrame([[
      predicted_close * np.random.uniform(0.99, 1.01), #Open
      predicted_close * np.random.uniform(1.00, 1.02), #High
      predicted_close * np.random.uniform(0.98, 1.00), #Low
      predicted_close, #Close
      predicted_close * np.random.uniform(0.98, 1.02), #Adj Close
      last_row.iloc[0]["Volume"] * np.random.uniform(0.98, 1.02), #Volume
      *last_row.iloc[0][[f"Close_lag_{lag}" for lag in range(1, 6)]].values.tolist(), #Close Lag 1-5
      *stock_df.iloc[-1].values
    ]], columns=feature_columns)

  plt.figure(figsize=(10, 6))
  plt.plot(future_df.index, future_df["Close"], label="Predicted Prices", color="orange")
  plt.title("Predicted Future Stock Prices (Next 30 Days)")
  plt.xlabel("Date")
  plt.ylabel("Price")
  plt.legend()
  plt.grid()
  plt.show()
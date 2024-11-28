#stl imports
import asyncio
from datetime import datetime
from time import sleep

#external library imports
import dearpygui.dearpygui as gui

#project imports
from classes.hashmap import *
from classes.trie import *
from data.datasets import *
import globals


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
  
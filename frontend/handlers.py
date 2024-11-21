#stl imports
from datetime import datetime
import asyncio
from time import sleep

#external library imports
import dearpygui.dearpygui as gui

#project imports
from datasets import *
from classes.trie import *
from globals import *


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
  pull()

def pull():
  sleep(0.1)
  loop = asyncio.new_event_loop()
  loop.run_until_complete(pull_stock_info(gui.get_value("search")))
  # update_graph()

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
  gui.set_value(progress_bar, 0)


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
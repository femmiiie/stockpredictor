#stl imports
from datetime import datetime
from time import sleep

#external library imports
import dearpygui.dearpygui as gui

#project imports
from classes.trie import *

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

def update_date_range():
    start_val = gui.get_value("start_date")
    end_val = gui.get_value("end_date")
    date_format = "%m/%d/%Y"

    start_date = datetime.strptime(start_val, date_format)
    end_date = datetime.strptime(end_val, date_format)

    if start_date > end_date:
      gui.set_value("start_date", end_date.strftime(date_format))
      gui.set_value("end_date", start_date.strftime(date_format))

#very basic state logic since the app only has 3 screens to deal with
def swap_visible_screen(swap_to : int):

  if swap_to == 1:
    gui.show_item("Primary")
    gui.set_primary_window("Primary", True)
    gui.hide_item("Credits")
    gui.hide_item("Predictor")

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

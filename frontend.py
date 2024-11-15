import dearpygui.dearpygui as gui
from globals import *
from trie import *
from time import sleep
from datetime import datetime, timedelta

def render_front(stocks : Trie):
  gui.create_context()
  gui.create_viewport(title="COP3530 Project 3", min_width=screen_size["width"], max_width=screen_size["width"], min_height=screen_size["height"] ,max_height=screen_size["height"])
  gui.setup_dearpygui()

  with gui.font_registry():
    default_font = gui.add_font("Arimo/Arimo-VariableFont_wght.ttf", 30)

  with gui.window(tag="Primary"):
    gui.bind_font(default_font)
    
    selector_setup(stocks)
    button_setup()
    range_setup()
    visualizer_setup()

  gui.show_viewport()
  gui.set_primary_window("Primary", True)
  gui.start_dearpygui()
  gui.destroy_context()

def button_setup():
  button_size = [150, 60]
  button_pos = [screen_size["width"] - button_size[0] - 50, screen_size["height"] - button_size[1] - 60]
  button = gui.add_button(label="Predict!", width=button_size[0], height=button_size[1])
  gui.set_item_pos(button, button_pos)

def selector_setup(stocks : Trie):
  gui.add_text("Select a Stock:")
  gui.add_input_text(tag="search", hint="Type to search...", width=210)
  gui.add_listbox(tag="dropdown", items=stocks.get_searched_list(""), callback=select_item, show=False, width=210)

  with gui.handler_registry():
    gui.add_key_release_handler(callback=(lambda: filter_options(stocks)))

  with gui.item_handler_registry(tag="search_reg") as handler:
    gui.add_item_active_handler(callback=show_listbox)
    gui.add_item_deactivated_handler(callback=hide_listbox)

  gui.bind_item_handler_registry("search", "search_reg")

def range_setup():
  gui.add_text("")
  gui.add_text("Prediction Range:")

  with gui.group(horizontal=True):
    gui.add_input_text(tag="start_date", default_value=datetime.now().strftime("%m/%d/%Y"), width=150)
    gui.add_text("-")
    gui.add_input_text(tag="end_date", default_value=(datetime.now() + timedelta(days=7)).strftime("%m/%d/%Y"), width=150)

  with gui.item_handler_registry(tag="range_reg") as handler:
    gui.add_item_deactivated_handler(callback=update_date_range)

  gui.bind_item_handler_registry("start_date", "range_reg")
  gui.bind_item_handler_registry("end_date", "range_reg")

def visualizer_setup():
  pass

def filter_options(stocks : Trie):
  input_text : str = gui.get_value("search").upper()
  filtered_items = [item for item in sorted(stocks.get_searched_list(input_text)) if input_text in item]
  gui.configure_item("dropdown", items=filtered_items)
  #print(filtered_items)

def show_listbox():
  gui.show_item("dropdown")

def hide_listbox():
  sleep(0.1)
  gui.hide_item("dropdown")

def select_item(sender):
  text = gui.get_value(sender)
  gui.set_value("search", text)

def update_date_range(sender):
    start_val = gui.get_value("start_date")
    end_val = gui.get_value("end_date")
    date_format = "%m/%d/%Y"

    start_date = datetime.strptime(start_val, date_format)
    end_date = datetime.strptime(end_val, date_format)

    if start_date > end_date:
      gui.set_value("start_date", end_date.strftime(date_format))
      gui.set_value("end_date", start_date.strftime(date_format))    
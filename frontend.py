import dearpygui.dearpygui as gui
from trie import *
from time import sleep

def render_front(stocks : Trie):
  gui.create_context()
  gui.create_viewport(title="COP3530 Project 3")
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
  button_size = [100, 40]
  window_size = [gui.get_viewport_client_width(), gui.get_viewport_client_height()]
  button_pos = [window_size[0] - button_size[0] - 50, window_size[1] - button_size[1] - 60]
  button = gui.add_button(label="Predict!", width=button_size[0], height=button_size[1])
  gui.set_item_pos(button, button_pos)

def selector_setup(stocks : Trie):
  gui.add_text("Select a Stock:")
  gui.add_input_text(tag="Search", hint="Type to search...", width=200)
  gui.add_listbox(tag="Dropdown", items=stocks.get_searched_list(""), callback=select_item, show=False, width=200)

  with gui.handler_registry():
    gui.add_key_release_handler(callback=(lambda: filter_options(stocks)))

  with gui.item_handler_registry(tag="search_reg") as handler:
    gui.add_item_active_handler(callback=show_listbox)
    gui.add_item_deactivated_handler(callback=hide_listbox)

  gui.bind_item_handler_registry("Search", "search_reg")

def range_setup():
  pass

def visualizer_setup():
  pass

def filter_options(stocks : Trie):
  input_text : str = gui.get_value("Search").upper()
  filtered_items = [item for item in sorted(stocks.get_searched_list(input_text)) if input_text in item]
  gui.configure_item("Dropdown", items=filtered_items)
  #print(filtered_items)

def show_listbox():
  gui.show_item("Dropdown")

def hide_listbox():
  sleep(0.1)
  gui.hide_item("Dropdown")

def select_item(sender):
  selected_item = gui.get_value(sender)
  gui.set_value("Search", selected_item)
  # gui.hide_item("Dropdown")

#stl imports
from datetime import datetime, timedelta

#external library imports
import dearpygui.dearpygui as gui

#project imports
from globals import *
from classes.trie import *
from frontend.handlers import *


def render_front(stocks : Trie):
  gui.create_context()
  gui.create_viewport(title="COP3530 Project 3", min_width=screen_size["width"], max_width=screen_size["width"], min_height=screen_size["height"] ,max_height=screen_size["height"])
  gui.setup_dearpygui()

  with gui.font_registry():
    default_font = gui.add_font("Arimo\Arimo-VariableFont_wght.ttf", 30)
    gui.bind_font(default_font)

  with gui.window(tag="Primary"):
    selector_setup(stocks)
    button_setup()
    range_setup()
    visualizer_setup()

  with gui.window(tag="Credits", show=False):
    credits_setup()

  with gui.window(tag="Predictor", show=False):
    pass

  gui.show_viewport()
  gui.set_primary_window("Primary", True)
  gui.start_dearpygui()
  gui.destroy_context()

def button_setup():
  button_size = [150, 60]
  predict_button_pos = [screen_size["width"] - button_size[0] - 50, screen_size["height"] - button_size[1] - 60]
  credits_button_pos = [screen_size["width"] - button_size[0] - 50, screen_size["height"] - 2*button_size[1] - 70]

  predict_button = gui.add_button(label="Predict!", width=button_size[0], height=button_size[1], callback=(lambda: swap_visible_screen(3)))
  credits_button = gui.add_button(label="Credits", width=button_size[0], height=button_size[1], callback=(lambda: swap_visible_screen(2)))

  gui.set_item_pos(predict_button, predict_button_pos)
  gui.set_item_pos(credits_button, credits_button_pos)

def selector_setup(stocks : Trie):
  gui.add_text("Select a Stock:")
  gui.add_input_text(tag="search", hint="Type to Search...", width=210)
  gui.add_listbox(tag="dropdown", items=stocks.get_searched_list(""), callback=select_item, show=False, width=210)

  with gui.handler_registry():
    gui.add_key_release_handler(callback=(lambda: filter_options(stocks)))

  with gui.item_handler_registry(tag="search_reg") as handler:
    gui.add_item_active_handler(callback=show_listbox)
    gui.add_item_deactivated_handler(callback=hide_listbox)

  gui.bind_item_handler_registry("search", "search_reg")

def range_setup():
  input_width = 150
  default_start_time = datetime.now().strftime("%m/%d/%Y")
  default_end_time = (datetime.now() + timedelta(days=7)).strftime("%m/%d/%Y")

  with gui.group(tag="range_group") as range:
    gui.add_text("")
    gui.add_text("Prediction Range:")

    #add_same_line is deprecated, so basic subgroup to get them all on the same line
    with gui.group(tag="range_input_group", horizontal=True):
      gui.add_input_text(tag="start_date", default_value=default_start_time, width=input_width)
      gui.add_text("-", tag="seperator")
      gui.add_input_text(tag="end_date", default_value=default_end_time, width=input_width)

    with gui.item_handler_registry(tag="range_reg"):
      gui.add_item_deactivated_handler(callback=update_date_range)

    gui.bind_item_handler_registry("start_date", "range_reg")
    gui.bind_item_handler_registry("end_date", "range_reg")

    #20 is an approximation for how much space the - char takes since it cannot be accessed directly on the first frame of runtime
    range_obj_width = 2*input_width + 20
    gui.set_item_pos(range, [screen_size["width"] - range_obj_width - 50, -30])

def visualizer_setup():
  graph_size = [400, 400]
  graph_pos = [10, screen_size["height"] - graph_size[1] - 60]

  with gui.plot(tag="visualizer", width=graph_size[0], height=graph_size[1]):
    gui.add_plot_axis(gui.mvXAxis, label="Date")
    gui.add_plot_axis(gui.mvYAxis, label="High Price for Day", tag="y-axis")

    gui.add_line_series(x=[0.5,1,2,3], y=[0.5,1,2,3], parent="y-axis")

  gui.set_item_pos("visualizer", graph_pos)

def credits_setup():
  gui.add_text("Created by the Soon to be Richest Team in COP3530")
  gui.add_text("Sandro Mocevic - Frontend Development")
  gui.add_text("Nouri Clarke - TBD")
  gui.add_text("Aimar Murua - TBD")

  button_size = [150, 60]
  back_button_pos = [screen_size["width"] - button_size[0] - 50, screen_size["height"] - button_size[1] - 60]
  back_button = gui.add_button(label="Back", width=button_size[0], height=button_size[1], callback=(lambda: swap_visible_screen(1)))
  gui.set_item_pos(back_button, back_button_pos)
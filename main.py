#stl imports
from os import path

#external library imports
import dearpygui.dearpygui as gui

#project imports
import frontend.frontend as frontend
import frontend.handlers as handlers
import classes.trie as trie
import classes.hashmap as hashmap
import datasets


def main():
  frontend.setup()

  gui.set_frame_callback(2, lambda: post_render_execution(stock_names))

  stock_names = trie.Trie()
  frontend.render_front(stock_names)


def post_render_execution(stock_names : trie.Trie):
  if not path.exists("stock_info.csv"):
    datasets.download_data()

  handlers.reset_loading_screen() #resets loading screen

  stock_list = datasets.get_stock_list()
  stock_names.insert_arr(stock_list)

  handlers.set_defaults(stock_names.get_first_item())
  handlers.swap_visible_screen(1) #swaps to main screen


"""
  preferred data format for proccessing
  list[str] of each name to pass into Trie

  Ex:
  stock_names[0] == "AAPL"
"""

if __name__ == "__main__":
  main()
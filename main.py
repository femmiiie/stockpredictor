#external library imports
import dearpygui.dearpygui as gui

#project imports
import classes.trie as trie
import datasets
import frontend.frontend as frontend
import frontend.handlers as handlers


def main():
  frontend.setup()

  #wont run if called normally after render_front, so put to a frame callback
  gui.set_frame_callback(2, lambda: post_render_execution(stock_names))

  stock_names = trie.Trie()
  frontend.render_front(stock_names)


def post_render_execution(stock_names : trie.Trie):
  datasets.download_data()

  handlers.reset_loading_screen() #resets loading screen
  stock_names.insert_arr(datasets.get_stock_list())
  handlers.set_defaults(stock_names.get_first_item())
  handlers.swap_visible_screen(1) #swaps to main screen


if __name__ == "__main__":
  main()
from os import path

# External library imports
import dearpygui.dearpygui as gui

# Project imports
import frontend.frontend as frontend
import frontend.handlers as handlers
import classes.trie as trie
import data.datasets as datasets


def main():
    frontend.setup()
    stock_names = trie.Trie()
    
    gui.set_frame_callback(2, lambda: post_render_execution(stock_names))
    frontend.render_front(stock_names)


def post_render_execution(stock_names : trie.Trie):
    datasets.download_data()

    handlers.reset_loading_screen()
    stock_names.insert_arr(datasets.get_stock_list())
    handlers.set_defaults(stock_names.get_first_item())
    handlers.swap_visible_screen(1)

if __name__ == "__main__":
  main()
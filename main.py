from os import path

# External library imports
import dearpygui.dearpygui as gui

# Project imports
import frontend.frontend as frontend
import frontend.handlers as handlers
import classes.trie as trie
import datasets
import globals
import asyncio


def main():
    frontend.setup()
    stock_names = trie.Trie()
    gui.set_frame_callback(2, lambda: post_render_execution(stock_names))
    frontend.render_front(stock_names)

    # Simplified for testing
    if not path.exists("stock_info.csv"):
        print("Error: stock_info.csv not found. Run datasets.download_data() first.")
        return

    # Get stock list and choose a stock for testing
    print(f"getting stocks")
    stock_list = datasets.get_stock_list()
    print(f"Available stocks: {stock_list}")
    print(f"got stocks")

    # stock_name = stock_list[0]  # Replace with desired stock or user input
    stock_name = "MMM"  # Replace with desired stock or user input
    print(f"Testing stock: {stock_name}")

    # Load stock data
    stk_data = asyncio.run(datasets.pull_stock_info(stock_name))
    print(stk_data)

    # Test the train_model function
    if globals.current_stock_data is not None:
        print("Calling train model")
        datasets.train_model(globals.current_stock_data)
        print("model trained")
    else:
        print("Error: No stock data loaded.")

# Function to test after GUI is disabled
def post_render_execution(stock_names):
    if not path.exists("stock_info.csv"):
        datasets.download_data()
    handlers.reset_loading_screen()
    stock_names.insert_arr(datasets.get_stock_list())
    handlers.set_defaults(stock_names.get_first_item())
    handlers.swap_visible_screen(1)

if __name__ == "__main__":
  main()
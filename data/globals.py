#stl imports
from asyncio import Lock

screen_size = {
  "width": 900,
  "height": 600
}

progress_bar = "prog"

#multiple disjunct areas of the code need to access this so this is the easiest way to store it
#using an asyncio lock to prevent multiple pieces of code accessing the data at the same time and breaking something
current_stock_data = None
data_lock = Lock()
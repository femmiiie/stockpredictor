import frontend.frontend as frontend
import classes.trie as trie

def main():
  #placeholder values to test search and selection functionality
  arr = ["word", "ward", "wart", "worry", "rat"]
  placeholder = trie.Trie()
  placeholder.insert_arr(arr)

  frontend.render_front(placeholder)

  #preferred data format for proccessing
  # list[str] of each name to pass into Trie
  # list[HashMap] for the daily info of each stock
  # keep the list 1-to-1 for easy indexing 

if __name__ == "__main__":
  main()
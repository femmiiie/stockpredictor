import frontend
import trie

def main():
  #placeholder values to test search and selection functionality
  placeholder = trie.Trie()
  placeholder.insert("word")
  placeholder.insert("ward")
  placeholder.insert("wart")
  placeholder.insert("worry")
  placeholder.insert("rat")

  frontend.render_front(placeholder)


if __name__ == "__main__":
  main()
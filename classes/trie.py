class Node:
  def __init__(self):
    self.children : dict = {}

class Trie:
  def __init__(self):
    self.root = Node()


  #basic trie insert
  def insert(self, string : str, index : int):
    curr_node = self.root
    string = string.upper()

    for char in string:
      if char not in curr_node.children:
        curr_node.children[char] = Node()

      curr_node = curr_node.children[char]

    curr_node.index = index

  
  def insert_arr(self, arr : list):
    for index, name in enumerate(arr):
      self.insert(name, index)


  def get_first_item(self):
    curr_node = self.root
    name = ""

    while curr_node.children:
      val = next(iter(curr_node.children.keys()))
      name += val
      curr_node = curr_node.children[val]


    return name


  def get_searched_list(self, starter : str) -> list:
    curr_node = self.root

    for char in starter:
      if char not in curr_node.children:
        return []
      
      curr_node = curr_node.children[char]
    
    return_arr = []
    self.searched_list_helper(return_arr, curr_node, starter)

    return return_arr


  def searched_list_helper(self, return_arr : list, curr_node : Node, string : str):
    if not curr_node.children:
      return_arr.append(string)
    else:
      for char in curr_node.children:
        self.searched_list_helper(return_arr, curr_node.children[char], string + char)
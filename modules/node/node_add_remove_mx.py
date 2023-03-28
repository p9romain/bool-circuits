class node_add_remove_mx:
  def add_child_id(self, i : int) -> None :
    """
    Adds the child of id [i] to the node : if it's already a child, add 1 to the multiplicity, else it just adds the child
    """
    if not isinstance(i, int):
      raise TypeError("Given argument must be an integer")

    if i in self.children:
      self.children[i] += 1
    else:
      self.children[i] = 1
            
    

  def add_parent_id(self, i : int) -> None :
    """
    Adds the parent of id [i] to the node : if it's already a parent, add 1 to the multiplicity, else it just adds the parent
    """
    if not isinstance(i, int):
      raise TypeError("Given argument must be an integer")

    if i in self.parents:
      self.parents[i] += 1
    else:
      self.parents[i] = 1
     
  

  def remove_parent_once(self, i : int) -> None :
    """
    Removes one to the multiplicity of the parent of id [i] : if it drops to 0, we get rid of it
    """
    if not isinstance(i, int):
      raise TypeError("Given argument must be an integer")
    
    if i in self.parents_ids:
      if self.parents[i] == 1: self.parents.pop(i)
      else: self.parents[i] -= 1
          
  

  def remove_parent_id(self, i : int) -> None :
    """
    Removes the parent of id [i]
    """
    if not isinstance(i, int):
      raise TypeError("Given argument must be an integer")
        
    if i in self.parents_ids: self.parents.pop(i)
      
  

  def remove_child_once(self, i : int) -> None :
    """
    Removes one to the multiplicity of the child of id [i] : if it drops to 0, we get rid of it
    """
    if not isinstance(i, int):
      raise TypeError("Given argument must be an integer")
    
    if i in self.children_ids:
      if self.children[i] == 1: self.children.pop(i)
      else: self.children[i] -= 1
          
  

  def remove_child_id(self, i: int) -> None :
    """
    Removes the child of id [i]
    """
    if not isinstance(i, int):
      raise TypeError("Given argument must be an integer")
        
    if i in self.children_ids: self.children.pop(i)
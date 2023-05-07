class bool_circ_simplify_mx:
  def simplify_assoc_xor(self, id : int) -> None : # focus on children xor node compared to parent copy node
    """
    Applies a certain simplification to a xor node (associativity)
    """
    if not isinstance(id, int):
      raise TypeError("Given id must be an integer")
    if not id in self.nodes_ids:
      raise Exception("Given id must be a node in the bool circuit")

    n = self.node_by_id(id)
    l = self.node_by_label_list(n.parents_ids, r"^\^$")
    if len(l) != 0:
      n_parent = l[0]
      for i, m in n_parent.parents.items():
        self.add_edge([(i, n.id)]*m)
        
      self.remove_node_by_id(n_parent.id)



  def simplify_assoc_copy(self, id : int) -> None : # focus on parent copy node compared to children copy node
    """
    Applies a certain simplification to a copys node (associativity)
    """
    if not isinstance(id, int):
      raise TypeError("Given id must be an integer")
    if not id in self.nodes_ids:
      raise Exception("Given id must be a node in the bool circuit")

    n = self.node_by_id(id)
    l = [ self.node_by_id(i) for i in n.children_ids if self.isCopyNode(i) ]
    if len(l) != 0:
      n_children = l[0]
      for i, m in n_children.children.items():
        self.add_edge([(n.id,i)]*m)
        
      self.remove_node_by_id(n_children.id)



  def simplify_invol_xor(self, id : int) -> None : # focus on xor node
    """
    Applies a certain simplification to a xor node (involution)
    """
    if not isinstance(id, int):
      raise TypeError("Given id must be an integer")
    if not id in self.nodes_ids:
      raise Exception("Given id must be a node in the bool circuit")

    n = self.node_by_id(id)
    l = [ self.node_by_id(i) for i in n.parents_ids if self.isCopyNode(i) ]
    if len(l) != 0:
      n_parent = l[0]
      m = n_parent.children[n.id]
      self.remove_parallel_edges((n_parent.id,n.id))

      if m%2 == 1:
        self.add_edge((n_parent.id,n.id))



  def simplify_invol_not(self, id : int) -> None : # focus on parent copy node compared to children copy node
    """
    Applies a certain simplification to a not node (involution)
    """
    if not isinstance(id, int):
      raise TypeError("Given id must be an integer")
    if not id in self.nodes_ids:
      raise Exception("Given id must be a node in the bool circuit")

    n = self.node_by_id(id)
    n_children = self.node_by_id(n.children_ids[0])

    if n_children.label in ["!", "~"]:
      self.add_edge((n.parents_ids[0],n_children.children_ids[0]))
      self.remove_node_by_id(n.id)
      self.remove_node_by_id(n_children.id)



  def simplify_delete(self, id : int) -> None : # focus on op node
    """
    Applies a certain simplification to a delete node : op -> copy
    """
    if not isinstance(id, int):
      raise TypeError("Given id must be an integer")
    if not id in self.nodes_ids:
      raise Exception("Given id must be a node in the bool circuit")

    n = self.node_by_id(id)
    if n.outdegree() == 1 and self.isCopyNode(n.children_ids[0]) and self.node_by_id(n.children_ids[0]).outdegree() == 0:
      for n_id in n.parents_ids:
        self.add_node("",{n_id:1},{})

      self.remove_node_by_id(n.children_ids[0])
      self.remove_node_by_id(n.id)



  def simplify_not_through_xor(self, id : int) -> None : # focus on xor node
    """
    Applies a certain simplification to a xor node : -> not -> xor ->
    """
    if not isinstance(id, int):
      raise TypeError("Given id must be an integer")
    if not id in self.nodes_ids:
      raise Exception("Given id must be a node in the bool circuit")

    n = self.node_by_id(id)
    l = self.node_by_label_list(n.parents_ids, r"^[~!]$")
    if len(l) != 0:
      n_parent = l[0]
      self.add_edge((n_parent.parents_ids[0],n.id))
      self.remove_node_by_id(n_parent.id)

      self.add_node(n_parent.label, {n.id:1}, {n.children_ids[0]:1})
      self.remove_edge((n.id, n.children_ids[0]))



  def simplify_not_through_copy(self, id : int) -> None : # focus on copy node
    """
    Applies a certain simplification to a xor node : -> not -> copy ->
    """
    if not isinstance(id, int):
      raise TypeError("Given id must be an integer")
    if not id in self.nodes_ids:
      raise Exception("Given id must be a node in the bool circuit")

    n = self.node_by_id(id)
    n_parent = self.node_by_id(n.parents_ids[0])

    if n_parent.label in ["~", "!"]:
      self.add_edge((n_parent.parents_ids[0],n.id))
      self.remove_node_by_id(n_parent.id)

      for n_children_id in n.children_ids:
        self.add_node(n_parent.label,{n.id:1},{n_children_id:1})
        self.remove_edge((n.id,n_children_id))



  def simplify_node(self, id : int) -> None :
    """
    Applies a certain simplify to a node
    """
    if not isinstance(id, int):
      raise TypeError("Given id must be an integer")
    if not id in self.nodes_ids:
      raise Exception("Given id must be a node in the bool circuit")

    label = self.node_by_id(id).label
    if label == "^":
      self.simplify_assoc_xor(id)
      self.simplify_invol_xor(id)
      self.simplify_not_through_xor(id)
    elif label == "":
      self.simplify_assoc_copy(id)
      self.simplify_not_through_copy(id)
    elif label in ["~","!"] :
      self.simplify_invol_not(id)

    # check if it isn't deleted
    if id in self.nodes_ids: # we check for each node, just in case
      self.simplify_delete(id)
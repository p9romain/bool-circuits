class bool_circ_transform_mx:
  def transform_copy(self, id : int):
    n = self.node_by_id(id)
    # invariant : n est un noeud copie
    if n.indegree() == 1 :
      n_parent = self.node_by_id(n.parents_ids[0])
      if n_parent.indegree() == 0 and (n_parent.label == "0" or n_parent.label == "1"):
        const = n_parent.label
        
        for i in n.children_ids:
          self.add_node(const, {}, {i:1})
          self.remove_edge((id,i))

        self.remove_node_by_id(n.parents_ids[0])
        self.remove_node_by_id(id)
      else:
        raise Exception("")
    else:
      raise Exception("")
    

    
  def transform_not(self, id : int):
    n = self.node_by_id(id)

    if  n.indegree() == 1 :
      n_parent = self.node_by_id(n.parents_ids[0])
      if n_parent.indegree() == 0 and (n_parent.label == "0" or n_parent.label == "1"):
        const = n_parent.label

        self.remove_node_by_id(n.parents_ids[0])
        n.label = "0" if const == "1" else "1"
      else:
        raise Exception("")
    else:
      raise Exception("")
    


  def transform_and(self, id : int):
    n = self.node_by_id(id)

    l = self.node_by_label_list(n.parents_ids, r"^[01]{1}$")
    if len(l) >= 1:
      n_parent_constant = None
      for i in l:
        if i.indegree() == 0 :
          n_parent_constant = i
          break
      if n_parent_constant is None: raise Exception("")

      const = n_parent_constant.label
      if const == "0":
        others_parent_ids = list(set(n.parents_ids) - set([n_parent_constant.id]))
        for i in others_parent_ids:
          self.add_node("", {i:1}, {})
          self.remove_edge((i,id))
        n.label = const
        self.remove_node_by_id(n_parent_constant.id)
      else:
        self.remove_node_by_id(n_parent_constant.id)
    else:
      self.transform_neutral(id)
    
  

  def transform_or(self, id : int):
    n = self.node_by_id(id)

    l = self.node_by_label_list(n.parents_ids, r"^[01]{1}$")
    if len(l) >= 1:
      n_parent_constant = None
      for i in l:
        if i.indegree() == 0 :
          n_parent_constant = i
          break
      if n_parent_constant is None: raise Exception("")

      const = n_parent_constant.label
      if const == "1":
        others_parent_ids = list(set(n.parents_ids) - set([n_parent_constant.id]))
        for i in others_parent_ids:
          self.add_node("", {i:1}, {})
          self.remove_edge((i,id))
        n.label = const
        self.remove_node_by_id(n_parent_constant.id)
      else:
        self.remove_node_by_id(n_parent_constant.id)
    else:
      self.transform_neutral(id)
    


  def transform_xor(self, id : int):
    n = self.node_by_id(id)

    l = self.node_by_label_list(n.parents_ids, r"^[01]{1}$")
    if len(l) >= 1:
      n_parent_constant = None
      for i in l:
        if i.indegree() == 0 :
          n_parent_constant = i
          break
      if n_parent_constant is None: raise Exception("")

      const = n_parent_constant.label
      if const == "1":
        self.add_node(label='~', parents={id:1}, children={n.children_ids[0]:1})
        self.remove_edge((id, n.children_ids[0]))
      self.remove_node_by_id(n_parent_constant.id)
    else:
      self.transform_neutral(id)
    


  def transform_neutral(self, id : int):
    n = self.node_by_id(id)

    if n.indegree() == 0 :
      if n.label in ['|', '||'] or n.label == '^' :
        n.label = '0'
      elif n.label in ['&', '&&'] :
        n.label = '1'
      else:
        raise Exception("")
    else:
      raise Exception("")
    


  def transform(self, id : int):
    label = self.node_by_id(id).label

    if label == "":
      self.transform_copy(id)
    elif label in ["~","!"]:
      self.transform_not(id)
    elif label in ["&","&&"]:
      self.transform_and(id)
    elif label in ["|","||"]:
      self.transform_or(id)
    elif label == "^":
      self.transform_xor(id)
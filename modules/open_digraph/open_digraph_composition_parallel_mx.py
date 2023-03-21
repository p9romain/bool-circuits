class open_digraph_composition_parallel_mx:
  def shift_indices(self, n : int) -> None :
    """
    Shifts all the ids of [n] (positive or negative)
    """
    if not isinstance(n, int):
      raise TypeError("Given argument must be an int")

    if self.min_id+n < 0: raise Exception("All the ids must be positive, even after the shift")

    def shift_indices_node(m):
      m.id += n
      m.parents = { k+n:v for (k,v) in m.parents.items() }
      m.children = { k+n:v for (k,v) in m.children.items() }
      return m

    self.nodes = { k+n:shift_indices_node(v) for (k,v) in self.nodes.items() }

    self.inputs_ids = [ i+n for i in self.inputs_ids ]
    self.outputs_ids = [ i+n for i in self.outputs_ids ]



  def iparallel(self, *args) -> None :
    """
    Adds the graph [g] in parallel of [self]
    """

    if len(args) == 0: raise Exception("")

    def f(g):
      g_copy = g.copy()
      g_copy.shift_indices(self.max_id-g_copy.min_id+1)
      
      self.desc = "Parallèle : " + self.desc + " & " + g_copy.desc
      self.nodes.update(g_copy.nodes)
      self.inputs_ids += g_copy.inputs_ids
      self.outputs_ids += g_copy.outputs_ids

    def fusion_list(l):
      for g in l:
        f(g)

    for arg in args:
      if (type(arg) == list): fusion_list(arg)
      else: fusion_list([arg])
  


  def icompose(self, f) -> None:
    """
    Composes the graph [f] in [self].
    Graphs must have the same number of inputs and ouputs ([self] comes after [f])
    """
    if len(self.inputs_ids) != len(f.outputs_ids):
      raise Exception("Number of inputs and outputs don't match")
        
    f_copy = f.copy()
    f_copy.shift_indices(self.max_id-f_copy.min_id+1)
    self.nodes.update(f_copy.nodes)
    
    for k,idk in enumerate(f_copy.outputs_ids):
      id_depart = self.node_by_id(idk).parent_ids[0]
      id_arrivee = self.node_by_id(self.inputs_ids[k]).children_ids[0]
      self.add_edge((id_depart,id_arrivee))
            
    self.remove_node_by_id(f_copy.outputs_ids)
    self.remove_node_by_id(self.inputs_ids)
    self.inputs_ids = f_copy.inputs_ids
   


  def connected_components(self):
    """
    Lists all the connected components of a graph. The dict looks like this :
    { node_id : 0, ..., node_id : 0, node_id : 1, ...., node_id : n }
    where 0, ..., n represents the id of the subgraph with nodes node_id, ..., node_id
    """
    comp = {}
    nodes_dict = self.nodes.copy()
    
    def pop_and_search(i, k):
      if i in nodes_dict:
        key_ids = set(list(nodes_dict.keys()))
        p_ids = nodes_dict[i].parent_ids
        p_ids = list(set(p_ids) & key_ids)
        c_ids = nodes_dict[i].children_ids
        c_ids = list(set(c_ids) & key_ids)
        del nodes_dict[i]
        comp[i] = k
        for t in p_ids: pop_and_search(t,k)
        for t in c_ids: pop_and_search(t,k)
    
    k = 0
    while len(nodes_dict) > 0:
      #ind = rd.choice(list(nodes_dict.keys())) (sûrement mieux mais pas possible pour les tests)
      ind = list(nodes_dict.keys())[0]
      pop_and_search(ind, k)
      k += 1
    
    return comp



  def connected_graphs(self):
    """
    Returns all the connected subgraphs in a list of graphs
    """
    comp = self.connected_components()
    l = []
    for k in list(set(comp.values())):
      nodes = [ self.node_by_id(i) for i, v in comp.items() if v == k ]
      inputs = [ i for i, v in comp.items() if v == k and i in self.inputs ]
      outputs = [ i for i, v in comp.items() if v == k and i in self.outputs ]
      l.append(self.__class__(inputs, outputs, nodes))
    return l 
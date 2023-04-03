import sys
import os
root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root) # allows us to fetch files from the project root

from typing import List
import random as rd

import modules.open_digraph.open_digraph as od
import modules.adjacency_matrix as am

class bool_circ(od.open_digraph):
  def __init__(self, inputs : List[int], outputs : List[int], nodes : iter, desc : str = "") -> None:
    '''
    inputs: int list; the ids of the input nodes
    outputs: int list; the ids of the output nodes
    nodes: node iter;
    desc: str;
    '''
    od.open_digraph.__init__(self, inputs, outputs, nodes, desc)
    if not self.is_well_formed(): raise Exception("Given argument must be a correct bool circuit")



  def is_well_formed(self) -> bool :
    """
    Check if the bool circuit is well formed :
    - the circuit must be acyclic
    - each AND, OR and XOR gates must have out-degree of 1
    - each NOT gates must have in-degree and out-degree of 1
    - each COPY gates must have in-degree of 1
    - each CST gates must have in-degree of 0
    - everything else isn't a correct node 
    """
    if not od.open_digraph.is_well_formed(self) : return False

    def node_well_formed(n):
      if n.label == '&' or n.label == '&&' :
        return n.outdegree() == 1
      if n.label == '|' or n.label == '||' :
        return n.outdegree() == 1
      if n.label == '^' :
        return n.outdegree() == 1
      if n.label == '~' or n.label == '!' :
        return n.indegree() == 1 and n.outdegree() == 1
      if n.label == '' :
        return n.indegree() == 1
      if n.label == '0' or n.label == '1' :
        return n.indegree() == 0
      else :
        return False

    # j'enlève les inputs et outputs
    for n in list(set(self.nodes_list) - set(self.outputs_list) - set(self.inputs_list)):
      if not node_well_formed(n): return False
      
    return not self.is_cyclic()



  def save_as_dot_file(self, path : str = "dot_files/bool_circ/bool_circ.dot", verbose : bool = False) -> None :
    """
    Saves the graph in a dot file
    The verbose adds the id in the file, not only the label of a node
    The add argument says if we add the graph at the end of the file
    """
    od.open_digraph.save_as_dot_file(self, path, verbose)   



  def save_as_pdf_file(self, path : str = "dot_files/bool_circ/bool_circ.dot", verbose : bool = False) -> str :
    """
    Saves the graph in a pdf file
    The verbose adds the id in the file, not only the label of a node
    The add argument says if we add the graph at the end of the file
    Returns the path of the pdf_file (useful for display)
    """
    return od.open_digraph.save_as_pdf_file(self, path, verbose)



  def display(self, path : str = "dot_files/bool_circ/bool_circ.dot", verbose : bool = False) -> None :
    """
    Saves and display the graph in a pdf
    The verbose adds the id in the file, not only the label of a node
    """
    od.open_digraph.display(self, path, verbose)

  def __str__(self) -> str :
    """
    Overload str conversion
    """
    return od.open_digraph.__str__(self)



  def __repr__(self) -> str :
    """
    Overload repr conversion (= str)
    """
    return self.__str__()

  @classmethod
  def from_str(cls, *args) :
    """
    """
    if len(args) == 0: raise Exception("An argument has to be given")
    
    def f(s, i):
      g = cls.empty()
      g.add_output_node(label="o"+str(i),id=0)
      g.add_node(children={0:1})

      cn = 1
      s_tmp = ''
      for c in s:
        if c == '(':
          g.node_by_id(cn).label += s_tmp
          cn = g.add_node('',{},{cn:1})
          s_tmp = ''
        elif c == ')':
          g.node_by_id(cn).label += s_tmp
          cn = g.node_by_id(cn).children_ids[0]
          s_tmp = ''
        else:
          s_tmp += c
      return g

    graphs = []
    for i, s in enumerate(args):
      graphs += [f(s, i)]

    if len(graphs) > 1 : graphs[0].iparallel(graphs[1:])
    g = graphs[0]
    g.desc = ""

    char = ["&", "&&", "|", "||", "~", "!", "^", "0", "1", " "] # j'ai rajouté le nom de l'output qu'on avait oublié de préciser
    merge_list = {}

    for n in g.nodes_list :
      if not n.label in char and n.label[0] != "o":
        if n.label in merge_list : merge_list[n.label] += [n.id]
        else: merge_list[n.label] = [n.id]

    for i in merge_list:
      if len(merge_list[i]) > 1:
        g.merge_nodes(merge_list[i])

      id_node = merge_list[i][0]
      g.node_by_id(id_node).label = ' '
      g.add_input_node(i,{id_node:1})

    return g, list(merge_list.keys())



  @classmethod
  def random(cls, n: int, bound : int, input : int, output : int) :
    """
    """
    # tester si bound < 2

    M = am.random_matrix(n, bound, null_diag = True, triangular = True)
    cls = am.graph_from_adjacency_matrix(M)

    # Inputs

    no_parents = [ n.id for n in cls.nodes_list if n.indegree() == 0 ]
    for id in no_parents :
      cls.add_input_node(children = {id:1})

    l = list(set(cls.nodes_list) - set(cls.outputs_list) - set(cls.inputs_list))
    if input > len(no_parents) :
      for _ in range(input-len(no_parents)):
        cls.add_input_node(children = {rd.sample(l, 1)[0].id : 1})

    def fi(id1, id2):
      idc1 = cls.node_by_id(id1).children_ids[0]
      idc2 = cls.node_by_id(id2).children_ids[0]

      id_cp = cls.add_node(children = {idc1:1, idc2:1}, parents = {id1: 1})
      cls.node_by_id(id1).children = {id_cp: 1}
      cls.remove_node_by_id(id2)

    while ( len(cls.inputs_ids) > input) :
      l = rd.sample(cls.inputs_ids, 2)
      fi(l[0], l[1])

    # Outputs

    no_children = [ n.id for n in cls.nodes_list if n.outdegree() == 0 ]
    for id in no_children :
      cls.add_output_node(parents = {id:1})
    
    l = list(set(cls.nodes_list) - set(cls.outputs_list) - set(cls.inputs_list))
    if output > len(no_children) :
      for _ in range(output-len(no_children)):
        cls.add_output_node(parents = {rd.sample(l, 1)[0].id : 1})

    def fo(id1, id2):
      idc1 = cls.node_by_id(id1).parents_ids[0]
      idc2 = cls.node_by_id(id2).parents_ids[0]

      id_bin = cls.add_node(parents = {idc1:1, idc2:1}, children = {id1: 1})
      cls.node_by_id(id1).parents = {id_bin: 1}
      cls.remove_node_by_id(id2)

    while ( len(cls.outputs_ids) > output) :
      l = rd.sample(cls.outputs_ids, 2)
      fo(l[0], l[1])

    # Labels

    l = list(set(cls.nodes_list) - set(cls.outputs_list) - set(cls.inputs_list))
    for n in l :
      in_deg = n.indegree()
      out_deg = n.outdegree()

      if in_deg == 1 and out_deg == 1 :
        n.label = '!'
      elif in_deg == 1 and out_deg > 1 :
        n.label = ' '
      elif in_deg > 1 and out_deg == 1 :
        n.label = rd.sample(['&&', '||', '^'], 1)[0]
      elif in_deg > 1 and out_deg > 1 :
        id_cp = cls.add_node(label = ' ', parents = {n.id : 1}, children = n.children.copy())
        n.children = {id_cp : 1}
        n.label = rd.sample(['&&', '||', '^'], 1)[0]

    return cls

  @classmethod
  def adder(cls, n : int):
    def bis(n):
      if n == 0:
        g, _ = bool_circ.from_str("((a0)&(b0))|(((a0)^(b0))&(c))", "((a0)^(b0))^(c)")
        for o in g.outputs_list:
          if o.label == "o0": o.label = "c'"
          elif o.label == "o1": o.label = "r0" 
        return g
      else:
        g1 = bool_circ.adder(n-1)
        g2 = g1.copy()

        for i in g2.inputs_list:
          if i.label[0] == 'a': i.label = "A" + i.label[1:]
          elif i.label[0] == 'b': i.label = "B" + i.label[1:]
          elif i.label[0] == 'c': i.label = "C"

        for i in g2.outputs_list:
          if i.label[0] == 'r': i.label = "R" + i.label[1:]
          elif i.label == "c'": i.label = "C'"

        g = od.open_digraph.parallel(g1,g2)

        # carry
        n_C_prime = g.node_by_label(r"C'")[0]
        n_c = g.node_by_label(r"^c$")[0]
        g.add_edge((n_C_prime.parents_ids[0], n_c.children_ids[0]))
        g.remove_node_by_id([n_C_prime.id,n_c.id])
        
        # rename a_i with a_{n+i} and A_i with a_i
        for i in g.node_by_label(r"[abr]+"):
          i.label = i.label[0] + str(int(i.label[1:])+n)
        for i in g.node_by_label(r"[ABR]+"):
          i.label = i.label.lower()
        g.node_by_label(r"C")[0].label = "c"

        return g

    cls = bis(n)
    return cls
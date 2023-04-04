import sys
import os
root = os.path.normpath(os.path.join(__file__, './../../..'))
sys.path.append(root) # allows us to fetch files from the project root

from typing import List, Dict, Tuple
import numpy as np
import generic_heap as gh
import copy as cp
import re

import modules.node.node as nd
import modules.open_digraph.open_digraph_add_remove_mx as od_mx1
import modules.open_digraph.open_digraph_classmethod_mx as od_mx2
import modules.open_digraph.open_digraph_composition_parallel_mx as od_mx3
import modules.open_digraph.open_digraph_path_mx as od_mx4
import modules.open_digraph.open_digraph_save_mx as od_mx5

class open_digraph(od_mx1.open_digraph_add_remove_mx, 
                   od_mx2.open_digraph_classmethod_mx, 
                   od_mx3.open_digraph_composition_parallel_mx, 
                   od_mx4.open_digraph_path_mx, 
                   od_mx5.open_digraph_save_mx): # for open directed graph
  def __init__(self, inputs : List[int], outputs : List[int], nodes : iter, desc : str = "") -> None:
    '''
    inputs: int list; the ids of the input nodes
    outputs: int list; the ids of the output nodes
    nodes: node iter;
    desc: str;
    new_id: int; an id not in the graph
    '''
    # Comme pour les dictionnaires plus haut
    if not isinstance(inputs, list):
      raise TypeError("Inputs must be a list")
    types = set(type(k) for k in inputs)
    if len(types) >= 1 and list(types)[0] != int :
      raise TypeError("Elements in inputs must all be integers")

    if not isinstance(outputs, list):
      raise TypeError("Outputs must be a list")
    types = set(type(k) for k in outputs)
    if len(types) >= 1 and list(types)[0] != int :
      raise TypeError("Elements in outputs must all be integers")

    # On teste si c'est un itérateur quelconque
    try:
      _ = (e for e in nodes) # oui oui cette syntaxe ne fonctionne qu'avec les itérateurs en fait
    except TypeError:
      raise TypeError("Nodes must be an iterator")
    # On teste si ça contient bien que des nodes
    types = set(type(k) for k in nodes)
    if len(types) >= 1 and list(types)[0] != nd.node :
      raise TypeError("Elements in nodes must all be nodes")

    if not isinstance(desc, str):
      raise TypeError("Description must be a string")

    self.__inputs_ids = inputs
    self.__outputs_ids = outputs
    self.__nodes = {node.id:node for node in nodes} # self.nodes: <int,node> dict
    self.__desc = desc



  @property
  def desc(self) -> str :
    """
    Getter for the descrption of the graph
    """
    return self.__desc



  # can be useful maybe   
  @property
  def inputs(self) -> Dict[int, nd.node] :
    """
    Getter for the graph's inputs (a dict {note id: node})
    """
    return { i:self.__nodes[i] for i in self.__inputs_ids }



  # can be useful maybe
  @property
  def inputs_list(self) -> List[nd.node] :
    """
    Getter for the graph's inputs
    """
    return [ self.__nodes[i] for i in self.__inputs_ids ]



  @property
  def inputs_ids(self) -> List[int] :
    """
    Getter for the graph's input's ids
    """
    return self.__inputs_ids



  # can be useful maybe    
  @property
  def outputs(self) -> Dict[int, nd.node] :
    """
    Getter for the graph's outputs (a dict {note id: node})
    """
    return { i:self.__nodes[i] for i in self.__outputs_ids }



  # can be useful maybe
  @property
  def outputs_list(self) -> List[int] :
    """
    Getter for the graph's outputs
    """
    return [ self.__nodes[i] for i in self.__outputs_ids ]



  @property
  def outputs_ids(self) -> List[int] :
    """
    Getter for the graph's output's ids
    """
    return self.__outputs_ids



  # id_nodes_map rename
  @property
  def nodes(self) -> Dict[int, nd.node] :
    """
    Getter for the graph's nodes (a dict {note id: node})
    """
    return self.__nodes



  # nodes rename
  @property
  def nodes_list(self) -> List[nd.node] :
    """
    Getter for the graph's nodes
    """
    return list(self.nodes.values())
      


  @property
  def nodes_ids(self) -> List[int] :
    """
    Getter for the graph's nodes' id
    """
    return list(self.nodes.keys())



  @property
  def min_id(self) -> int :
    """
    Getter for the minimal id in the graph
    """
    if self.nodes_ids == []:
      raise Exception("Graph hasn't any nodes")

    return min(self.nodes_ids)



  @property
  def max_id(self) -> int :
    """
    Getter for the maximal id in the graph
    """
    if self.nodes_ids == []:
      raise Exception("Graph hasn't any nodes")

    return max(self.nodes_ids)



  @property
  def new_id(self) -> int :
    """
    Getter for an id which isn't in the graph
    """
    return list(set(range(self.min_id, self.max_id+2))-set(self.nodes_ids))[0] if self.nodes_ids != [] else 0



  @property
  def edges(self) -> List[Tuple[int, int]]:
    """
    Getter for all the edges in a list of (node id, node id)
    A tuple can appear several times for each edge
    """
    E = []
    for n in self.nodes_list:
      for key, value in n.children.items():
        for _ in range(value):
          E.append((n.id, key))
    return E



  @inputs_ids.setter
  def inputs_ids(self, i : List[int]) -> None :
    """
    Setter for the inputs ids
    """
    if not isinstance(i, list):
      raise TypeError("Given argument must be a list")
    types = set(type(k) for k in i)
    if len(types) >= 1 and list(types)[0] != int :
      raise TypeError("Elements in the given argument must all be integers")

    for k in i :
      if not k in self.nodes_ids:
        raise Exception("Given input isn't in the graph")

    self.__inputs_ids = i
      


  @outputs_ids.setter
  def outputs_ids(self, o : List[int]) -> None :
    """
    Setter for the outputs ids
    """
    if not isinstance(o, list):
      raise TypeError("Given argument must be a list")
    types = set(type(k) for k in o)
    if len(types) >= 1 and list(types)[0] != int :
      raise TypeError("Elements in the given argument must all be integers")

    for k in o :
      if not k in self.nodes_ids:
        raise Exception("Given output isn't in the graph")

    self.__outputs_ids = o



  @desc.setter
  def desc(self, desc : str) -> None :
    """
    Setter for the description of the grph
    """
    if not isinstance(desc, str):
      raise Exception("The description must be a string")

    self.__desc = desc


  
  @nodes.setter
  def nodes(self, nodes : Dict[int, nd.node]) -> None :
    """
    Setter for the nodes (because of mixins)
    """
    if not isinstance(nodes, dict):
      raise TypeError("Given argument must be a list")
    types = set(type(k) for k in nodes.keys())
    if len(types) >= 1 and list(types)[0] != int :
      raise TypeError("Elements in the given argument must all be integers")
    types = set(type(k) for k in nodes.values())
    if len(types) >= 1 and list(types)[0] != nd.node :
      raise TypeError("Elements in the given argument must all be integers")
    
    self.__nodes = nodes



  #pour les sets
  def __hash__(self) -> hash :
    return hash(self.desc*sys.getsizeof(self))



  def __str__(self) -> str :
    """
    Overload str conversion
    """
    V = [ v.label for v in self.nodes_list ]
    I = [ self.nodes[i].label for i in self.inputs_ids ]
    O = [ self.nodes[i].label for i in self.outputs_ids ]
    E = [ (self.node_by_id(a).label, self.node_by_id(b).label) for a, b in self.edges ]
    desc = " : " + self.desc + " " if self.desc != "" else ""
    return f"[Graph{desc}] (V = {V}, I = {I}, O = {O}, E = [{E}])"



  def __repr__(self) -> str :
    """
    Overload repr conversion (= str)
    """
    return self.__str__()


      
  def __eq__(self, g) -> bool :
    """
    Overload eq operator
    """
    b1 = set(self.inputs_ids) == set(g.inputs_ids)
    b2 = set(self.outputs_ids) == set(g.outputs_ids)
    b3 = set(self.nodes_list) == set(g.nodes_list)
    return b1 and b2 and b3



  def __neq__(self, g) -> bool :
    """
    Overload beq operator
    """
    return not(self == g)



  def copy(self):
    """
    Overload copy operator
    """
    return cp.deepcopy(self)
      


  def node_by_id(self, i : int) -> nd.node :
    """
    ''Getter'' for the graph's node of id [i]
    """
    if not isinstance(i, int):
      raise TypeError("Given argument must be an integer")

    return self.nodes[i]
      


  def nodes_by_ids(self, l : List[int]) -> Dict[int, nd.node] :
    """
    ''Getter'' for the graph's nodes of ids [l]
    """
    if not isinstance(l, list):
      raise TypeError("Given argument must be a list")
    types = set(type(k) for k in l)
    if len(types) >= 1 and list(types)[0] != int :
      raise TypeError("Elements in the given argument must all be integers")

    return { i:self.nodes[i] for i in l }
    # on renvoie un dictionnaire comme ça c'est plus simple pour retrouver 
    # le noeud d'id i, vu que c'est une hash table

  def node_by_label(self, r):
    return [ n for n in self.nodes_list if re.search(r, n.label) ]

  def is_well_formed(self) -> bool :
    """
    Check if the graph is well formed :
    - each inputs_ids and outputs_ids nodes must be in the graph, i.e in [self.__nodes]
    - each inputs_ids must have only one child
    - each outputs_ids must have only one parent
    - each keys in the dict [self.__nodes] must be the same as the id of the nodes of its value
    - if a node 'n' has a child with a multiplicity 'm', then the child must have 'n' as a parent with multiplicity 'm'
    - if a node 'n' has a parent with a multiplicity 'm', then the parent must have 'n' as a child with multiplicity 'm'
    """
    b_inputs_ids = all(item in self.nodes_ids for item in self.inputs_ids)
    b_outputs_ids = all(item in self.nodes_ids for item in self.outputs_ids)
    b_inputs_ids_only_one_child = all(len(n.children_ids) == 1 and n.children[n.children_ids[0]] == 1 for n in self.nodes_by_ids(self.inputs_ids).values())
    b_outputs_ids_only_one_child = all(len(n.parents_ids) == 1 and n.parents[n.parents_ids[0]] == 1 for n in self.nodes_by_ids(self.outputs_ids).values())
    b_nodes = all(e for e in [ i == n.id for (i, n) in self.nodes.items() ])
    def assert_children(n):
      return all(self.node_by_id(i).parents[n.id] == m for (i, m) in n.children.items())
    def assert_parents(n):
      return all(self.node_by_id(i).children[n.id] == m for (i, m) in n.parents.items())
    b_mul = all(assert_children(n) and assert_parents(n) for n in self.nodes_list)
    
    return b_inputs_ids and b_outputs_ids and b_inputs_ids_only_one_child and b_outputs_ids_only_one_child and b_nodes and b_mul



  def assert_is_well_formed(self) -> bool :
    """
    Return if a graph is well formed, else it throws an exception
    """
    if self.is_well_formed(): return True
    else: raise Exception("Graph is not well formed.")



  def is_cyclic(self) -> bool :
    """
    Check if the graph is cyclic or not
    """
    g = self.copy()
    heap = gh.Heap([ (n.outdegree(), n.id) for n in g.nodes_list])

    def is_cyclic_bis(h):
      if h.empty(): return False
      elif h.peek()[0] != 0: return True
      else: 
        g.remove_node_by_id(h.pop()[1])
        h = gh.Heap([ (n.outdegree(), n.id) for n in g.nodes_list])
        return is_cyclic_bis(h)

    return is_cyclic_bis(heap)



  def assert_is_cycle(self) -> bool :
    if self.is_cyclic(): return True
    else: raise Exception("Graph is not well formed.")



  def ids_for_adjacency_matrix(self) -> Dict[int, int] :
    """
    Returns the ids of nodes who aren't inputs or outputs, where the result is a dict with { id node : new id in the matrix }
    """
    s = set(self.nodes_ids) - set(self.inputs_ids) - set(self.outputs_ids)
    return { i:l for i,l in enumerate(list(s)) } # on inverse l'id du noeud et l'entier pour la fonction adjacency_matrix



  def adjacency_matrix(self) -> np.ndarray :
    """
    Returns the adjacency matrix of the graph
    """
    s = self.ids_for_adjacency_matrix()
    def f(i, j):
      c = self.node_by_id(s[i]).children
      if s[j] in c:
        return c[s[j]]
      else:
        return 0
    return np.array( [ [ f(i, j) for j in range(len(s)) ] for i in range(len(s)) ] )
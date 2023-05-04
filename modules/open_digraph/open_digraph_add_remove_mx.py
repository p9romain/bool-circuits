import sys
import os
root = os.path.normpath(os.path.join(__file__, './../../..'))
sys.path.append(root) # allows us to fetch files from the project root

from typing import List, Dict, Tuple

import modules.node.node as nd

class open_digraph_add_remove_mx:
  def add_input_id(self, i : int) -> None :
    """
    Adds the node of id [i] as an input 
    """
    if not isinstance(i, int):
        raise TypeError("Given argument must be an integer")
    if i not in self.nodes_ids :
        raise Exception("Given id must be in the graph")

    if not i in self.inputs_ids:
        self.inputs_ids.append(i)
            
    

  def add_output_id(self, i : int) -> None:
    """
    Adds the node of id [i] as an output 
    """
    if not isinstance(i, int):
        raise TypeError("Given argument must be an integer")
    if i not in self.nodes_ids :
        raise Exception("Given id must be in the graph")

    if not i in self.outputs_ids:
        self.outputs_ids.append(i)



  def add_node(self, label : str = '', parents : Dict[int, int] = None, children : Dict[int, int] = None, id : int = None) -> int :
    """
    Adds a node with given argument (label and its parents and children)
    It also generates all the edges bewteen the node and its 'family'
    """
    if id != None and not isinstance(id, int):
        raise TypeError("Label must be a string")
    if id in self.nodes_ids:
        raise Exception("Given id must not already be in the graph")

    if not isinstance(label, str):
        raise TypeError("Label must be a string")
    if parents != None :
        if not isinstance(parents, dict):
            raise TypeError("Parents must be a dictionnary (or None)")
        types = set(type(k) for k in parents.keys())
        if len(types) >= 1 and list(types)[0] != int :
            raise TypeError("The keys of parents must all be integers")
        types = set(type(k) for k in parents.values())
        if len(types) >= 1 and list(types)[0] != int :
            raise TypeError("The values of parents must all be integers")

    if children != None :
        if not isinstance(children, dict):
            raise TypeError("Children must be a dictionnary (or None)")
        types = set(type(k) for k in children.keys())
        if len(types) >= 1 and list(types)[0] != int :
            raise TypeError("The keys of children must all be integers")
        types = set(type(k) for k in children.values())
        if len(types) >= 1 and list(types)[0] != int :
            raise TypeError("The values of children must all be integers")

    def f(l):
        if l is None: l = {}
        else:
            # par sécurité
            notin = list(set(l.keys()) - set(self.nodes_ids))
            for key in notin:
                del l[key]
        return l

    parents = f(parents)
    children = f(children)

    id = self.new_id if id == None else id
    n = nd.node(id, label, {}, {})
    
    self.nodes[n.id] = n
    
    self.add_edge( [ (i, n.id) for i in parents.keys() for _ in range(parents[i]) ] )
    self.add_edge( [ (n.id, i) for i in children.keys() for _ in range(children[i]) ] )

    return n.id

    

  def add_input_node(self, label : str = '', children : Dict[int, int] = None, id : int = None) -> int :
    """
    Adds an intput node with given argument (label and its children)
    It also generates all the edges bewteen the node and its children
    """
    if not isinstance(label, str):
        raise TypeError("Label must be a string")
    if children != None :
        if not isinstance(children, dict):
            raise TypeError("Children must be a dictionnary (or None)")
        types = set(type(k) for k in children.keys())
        if len(types) >= 1 and list(types)[0] != int :
            raise TypeError("The keys of children must all be integers")
        types = set(type(k) for k in children.values())
        if len(types) >= 1 and list(types)[0] != int :
            raise TypeError("The values of children must all be integers")
        
        if len(children) > 1 :
            raise Exception("Children must have at most one element")
        if children != {}:
            if not list(children.keys())[0] in self.nodes_ids :
                raise Exception("Given child must be in the graph")
            if list(children.values())[0] != 1 :
                raise Exception("Given child must have multiplicity of one")

    nodeId = self.add_node(label, None, children, id)
    self.add_input_id(nodeId)
    return nodeId


  
  def add_output_node(self, label : str = '', parents : Dict[int, int] = None, id : int = None) -> int :
    """
    Adds an output node with given argument (label and its parents)
    It also generates all the edges bewteen the node and its parents
    """
    if not isinstance(label, str):
        raise TypeError("Label must be a string")
    if parents != None :
        if not isinstance(parents, dict):
            raise TypeError("Parents must be a dictionnary (or None)")
        types = set(type(k) for k in parents.keys())
        if len(types) >= 1 and list(types)[0] != int :
            raise TypeError("The keys of parents must all be integers")
        types = set(type(k) for k in parents.values())
        if len(types) >= 1 and list(types)[0] != int :
            raise TypeError("The values of parents must all be integers")

        if len(parents) > 1 :
            raise Exception("Parents must have at most one element")
        if parents != {} :
            if not list(parents.keys())[0] in self.nodes_ids :
                raise Exception("Given parent must be in the graph")
            if list(parents.values())[0] != 1 :
                raise Exception("Given parent must have multiplicity of one")

    nodeId = self.add_node(label, parents, None, id)
    self.add_output_id(nodeId)
    return nodeId



  def add_edge(self, args : List[Tuple[int, int]] or Tuple[int, int]) -> None :
    """
    Adds one edge between one or several nodes' pair (src -> tgt)

    NON-ORIENTED GRAPH 
    """
    def f(src : int, tgt : int) -> None:
        if not src in self.nodes_ids :
            raise Exception(f'The source node with id {src} does not exist.')
        if not tgt in self.nodes_ids:
            raise Exception(f'The target node with id {tgt} does not exist.')


        self.node_by_id(src).add_child_id(tgt)
        self.node_by_id(tgt).add_parent_id(src)

    if isinstance(args, list) :
        types = set(type(k) for k in args)
        if len(types) >= 1 and list(types)[0] != tuple :
            raise TypeError("Elements in the given argument must all be tuples")
        if args != [] and ( len(args[0]) != 2 or not isinstance(args[0][0], int) or not isinstance(args[0][1], int) ) :
            raise TypeError("Elements in the given argument must all be tuples of two integers")
        for arg in args: f(arg[0],arg[1])

    elif isinstance(args, tuple) : 
        if len(args) != 2 or not isinstance(args[0], int) or not isinstance(args[0], int) :
            raise TypeError("Given argument must all be tuples of two integers")
        f(args[0],args[1])

    else:
        raise TypeError("Given argument must be a list of tuples of two integers, or just one tuple of two integers")
  


  def remove_edge(self, args : List[Tuple[int, int]] or Tuple[int, int]) -> None :
    """
    Removes one edge between one or several nodes' pair (src -> tgt)

    NON-ORIENTED GRAPH 
    """
    def f(src : int, tgt : int) -> None:
        if (not src in self.nodes_ids or not tgt in self.nodes_ids):
            raise Exception(f'The node with id {src} or {tgt} does not exist.')

        self.node_by_id(src).remove_child_once(tgt)
        self.node_by_id(tgt).remove_parent_once(src)
    
    if isinstance(args, list) :
        types = set(type(k) for k in args)
        if len(types) >= 1 and list(types)[0] != tuple :
            raise TypeError("Elements in the given argument must all be tuples")
        if args != [] and ( len(args[0]) != 2 or not isinstance(args[0][0], int) or not isinstance(args[0][1], int) ) :
            raise TypeError("Elements in the given argument must all be tuples of two integers")
        for arg in args: f(arg[0],arg[1])

    elif isinstance(args, tuple) : 
        if len(args) != 2 or not isinstance(args[0], int) or not isinstance(args[0], int) :
            raise TypeError("Given argument must all be tuples of two integers")
        f(args[0],args[1])

    else:
        raise TypeError("Given argument must be a list of tuples of two integers, or just one tuple of two integers")
  

     
  def remove_parallel_edges(self, args : List[Tuple[int, int]] or Tuple[int, int]) -> None :
    """
    Removes all the edges between one or several nodes' pair (src -> tgt)

    NON-ORIENTED GRAPH 
    """
    def f(src : int, tgt : int) -> None:
      if (not src in self.nodes_ids or not tgt in self.nodes_ids):
          raise Exception(f'The node with id {src} or {tgt} does not exist.')

      self.node_by_id(src).remove_child_id(tgt)
      self.node_by_id(tgt).remove_parent_id(src)

    if isinstance(args, list) :
      types = set(type(k) for k in args)
      if len(types) >= 1 and list(types)[0] != tuple :
        raise TypeError("Elements in the given argument must all be tuples")
      if args != [] and ( len(args[0]) != 2 or not isinstance(args[0][0], int) or not isinstance(args[0][1], int) ) :
        raise TypeError("Elements in the given argument must all be tuples of two integers")
      for arg in args: f(arg[0],arg[1])
        
    elif isinstance(args, tuple) : 
      if len(args) != 2 or not isinstance(args[0], int) or not isinstance(args[0], int) :
          raise TypeError("Given argument must all be tuples of two integers")
      f(args[0],args[1])

    else:
      raise TypeError("Given argument must be a list of tuples of two integers, or just one tuple of two integers")

  

  def remove_node_by_id(self, args : List[int] or int) -> None:
    """
    Removes the node of the give id (or several nodes with a id list) 
    """
    def f(i : int) -> None:
      for j in self.node_by_id(i).parents_ids:
          self.remove_parallel_edges((j, i))
          
      for j in self.node_by_id(i).children_ids:
          self.remove_parallel_edges((i, j))
          
      if i in self.inputs_ids: self.inputs_ids.remove(i)
      if i in self.outputs_ids: self.outputs_ids.remove(i)
      
      self.nodes.pop(i)
    
    if isinstance(args, list) :
      types = set(type(k) for k in args)
      if len(types) >= 1 and list(types)[0] != int :
        raise TypeError("Elements in the given argument must all be integers")
      
      for arg in args.copy(): f(arg)

    elif isinstance(args, int) : 
      f(args)

    else:
      raise TypeError("Given argument must be a list of integers, or just one integer")
    


  def merge_nodes(self, ids : List[int]) -> None :
    """
    Merges all the nodes in [ids]
    """
    if not isinstance(ids, list):
      raise TypeError("Given list must be a list")
    types = set(type(k) for k in ids)
    if len(types) >= 1 and list(types)[0] != int :
      raise TypeError("Elements in the given list must all be integers")
    for id in ids :
      if not id in self.nodes_ids:
        raise Exception("Given list must only have ids in the graph")

    if len(ids) < 2 : 
        raise Exception("At least two arguments must be given")

    def f(id1, id2):
      if id1 in self.inputs_ids or id1 in self.outputs_ids or id2 in self.inputs_ids or id2 in self.outputs_ids :
        raise Exception("Given ids must not be an input or an output")

      n1 = self.node_by_id(id1)
      n2 = self.node_by_id(id2)

      self.add_edge([ (n, id1) for n, m in n2.parents.items() for _ in range(m) ]+[ (id1, n) for n, m in n2.children.items() for _ in range(m) ])
      self.remove_node_by_id(id2)

    f(ids[0], ids[1])
    l = [ids[0]] + ids[2:]
    if len(l) > 1 : self.merge_nodes(l)
import sys
import os
root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root) # allows us to fetch files from the project root

from typing import List

import modules.open_digraph.open_digraph as od

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
    for n in list(set(self.nodes_list) - set(self.outputs.values()) - set(self.inputs.values())):
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



  @classmethod
  def from_str(cls, *args) :
    """
    """
    if len(args) == 0: raise Exception("")
    
    def f(s):
      g = cls.empty()
      g.add_output_node(id=0)
      g.add_node(children={0:1})
      g.desc = s

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
    graphs = []
    for i in range(len(args)):
      graphs += [f(i)]
    
    graphs[0].iparallel(graphs[1:])
    g = graphs[0]

    char = ["&", "&&", "|", "||", "~", "!", "^", "0", "1", " "]
    merge_list = {}

    for n in g.nodes_list :
      if not n.label in char:
        if n.label in merge_list : merge_list[n.label] += [n.id]
        else: merge_list[n.label] = [n.id]
    
    for i in merge_list:
      if len(merge_list[i]) > 1:
        od.open_digraph.merge_nodes(cls, merge_list[i])

      id_node = merge_list[i][0]
      g.node_by_id(id_node).label = ' '
      g.add_input_node(i,{id_node:1})

    return g, merge_list.keys()
import sys
import os
root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root) # allows us to fetch files from the project root

from typing import List, Dict, Tuple

import modules.open_digraph as od

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


  def save_as_dot_file(self, path : str = "dot_files/bool_circ.dot", verbose : bool = False) -> None :
    """
    Saves the graph in a dot file
    The verbose adds the id in the file, not only the label of a node
    The add argument says if we add the graph at the end of the file
    """
    od.open_digraph.save_as_dot_file(self, path, verbose)   



  def save_as_pdf_file(self, path : str = "dot_files/bool_circ.dot", verbose : bool = False) -> str :
    """
    Saves the graph in a pdf file
    The verbose adds the id in the file, not only the label of a node
    The add argument says if we add the graph at the end of the file
    Returns the path of the pdf_file (useful for display)
    """
    od.open_digraph.save_as_pdf_file(self, path, verbose)



  def display(self, path : str = "dot_files/bool_circ.dot", verbose : bool = False) -> None :
    """
    Saves and display the graph in a pdf
    The verbose adds the id in the file, not only the label of a node
    """
    od.open_digraph.display(self, path, verbose)

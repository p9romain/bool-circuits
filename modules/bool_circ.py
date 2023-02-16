import sys
import os
root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root) # allows us to fetch files from the project root

from typing import List, Dict, Tuple

import modules.open_digraph as od

class bool_circ(od.open_digraph):
  def __init__(self, g : od.open_digraph) -> None :
    '''
    inputs: int list; the ids of the input nodes
    outputs: int list; the ids of the output nodes
    nodes: node iter;
    desc: str;
    new_id: int; an id not in the graph
    '''
    if not isinstance(g, od.open_digraph):
      raise TypeError("Given argument must be an open digraph")

    super.__init__(g.inputs_ids, g.outputs_ids, g.nodes_list, g.desc)
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
    def node_well_formed(n):
      match n.label:
        case '&', '&&' :
          return n.outdegree() == 1
        case '|', '||' :
          return n.outdegree() == 1
        case '^' :
          return n.outdegree() == 1
        case '~', '!' :
          return n.indegree() == 1 and n.outdegree() == 1
        case '' :
          return n.indegree() == 1
        case '0', '1' :
          return n.indegree() == 0
        case _ :
          return False

    for n in self.nodes_list :
      if not node_well_formed(n): return False

    return not self.is_cyclic()
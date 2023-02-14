import sys
import os
root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root) # allows us to fetch files from the project root

from typing import List, Dict, Tuple

import modules.open_digraph as od

class bool_circ(od.open_digraph):
  def __init__(self, g):
    super.__init__(g.inputs_ids, g.outputs_ids, g.nodes_list, g.desc)
    if !self.is_well_formed(): raise Exception("")

  def is_well_formed(self):
    def node_well_formed(n):
      match n.label:
        case '&', '&&':
          return n.outdegree() == 1
        case '|', '||':
          return n.outdegree() == 1
        case '~':
          return n.indegree() == 1 and n.outdegree() == 1
        case '':
          return n.indegree() == 1
        case '0', '1':
          return n.indegree() == 0
        case _:
          return False

    for n in self.nodes_list:
      if !node_well_formed(n): return False

    return !self.is_cyclic()
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
        
      match n.label:
        case '&' | '&&' :
          return n.outdegree() == 1
        case '|' | '||' :
          return n.outdegree() == 1
        case '^' :
          return n.outdegree() == 1
        case '~' | '!' :
          return n.indegree() == 1 and n.outdegree() == 1
        case '' :
          return n.indegree() == 1
        case '0' | '1' :
          return n.indegree() == 0
        case _ :
          return False

    # j'enlève les inputs et outputs
    for n in list(set(self.nodes_list) - set(self.outputs.values()) - set(self.inputs.values())):
      if not node_well_formed(n): return False
      
    return not self.is_cyclic()



  def display(self, path : str = "dot_files/bool_circ.dot", verbose : bool = False) -> None :
        """
        Saves and display the graph in a pdf
        The verbose adds the id in the file, not only the label of a node
        """
        if not isinstance(path, str):
            raise Exception("The path must be a string")
        if not isinstance(verbose, bool):
            raise Exception("The verbose must be a bool")

        # On ne peut pas juste choper le point car si on est dans des répertoires .name, ça va tout casser donc on fait cette horreur :
        #   (on split avec les /, et on prend tout les éléments avant le dernier /) 
        # + (on split avec les /, on prendre le dernier (donc nom du fichier), et on remplace le .dot par .pdf)
        n_path = (''.join(str(e)+"/" for e in path.split("/")[:-1]))+"output/"+(path.split("/")[-1].split(".")[0]+".pdf")

        self.save_as_dot_file(path, verbose)
        os.system(f"dot -Tpdf \"{path}\" -Glabel=\"{self.desc}\" -o \"{n_path}\"")
        os.system(f"xdg-open \"{n_path}\"")

import sys
import os
root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root) # allows us to fetch files from the project root

from typing import List
import generic_heap as gh

import modules.open_digraph.open_digraph as od
import modules.adjacency_matrix as am
import modules.bool_circ.bool_circ_classmethod_mx as bc_mx1
import modules.bool_circ.bool_circ_transform_mx as bc_mx2
import modules.bool_circ.bool_circ_simplify_mx as bc_mx3

class bool_circ(bc_mx1.bool_circ_classmethod_mx,
                bc_mx2.bool_circ_transform_mx,
                bc_mx3.bool_circ_simplify_mx,
                od.open_digraph):
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
    for n in self.nodes_not_io_list:
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



  def __repr__(self) -> str :
    """
    Overload repr conversion (= str)
    """
    return self.__str__()


  
  def evaluate(self, n : int or str) -> str :
    """
    Evaluates the bool circuit with a certain int or str (binary).
    
    ----

    Example : ( x1 and x2 ) or x1

    If we give "11", it will evaluate the graph and returns ( 1 and 1 ) or 1 which 1, so "1"

    Example : ( x1 and x2 ) xor x2, ( x1 and x2 ) xor (not x1)

    If we give "01", it returns "1" and "1", so "11"
    """
    if not isinstance(n, str) and not isinstance(n, int):
      raise TypeError("Given argument must be an int or a binary int (str)")

    b = self.copy() # copy to not modify self
    if isinstance(n, str): n = int(n, 2) # we can just give binary string
    # exemple : for adder with 15 + 3 => "1111" + "0011" => "11110011" instead of giving 243

    n = self.from_int(n, len(b.inputs_ids)) # from int to bool_circ
    b = self.compose(n, b) # adding the int at the top of the bool_circ

    def f(n): # check if there isnt an output in [n]'s children 
      for id in n.children_ids:
        if id in b.outputs_ids : return False
      return True

    # for all co_leaves not attached to (at least) an output
    l = [ n for n in b.nodes_list if len(n.parents_ids) == 0 and f(n) ]

    while len(l) > 0 :
      n = l[0]
      
      # always an 0 or 1, but sometimes binary operator
      # eg : true && true && true => && with transform
      if n.label in ["0", "1"] : b.transform_node(n.children_ids[0])
      else : b.transform_neutral(n.id) 
      l = [ n for n in b.nodes_list if len(n.parents_ids) == 0 and f(n) ] # update what to do

    # to get result
    s = ""
    for o in b.outputs_list:
      lb = b.node_by_id(o.parents_ids[0]).label

      # always an 0 or 1, but sometimes binary operator
      # eg : true && true && true => && with transform
      if not lb in ["0", "1"] : b.transform_neutral(o.parents_ids[0])
      s += b.node_by_id(o.parents_ids[0]).label

    return s



  def evaluateHalfAdder(self, n : int, m : int) -> int :
    """
    Adds [n] to [m]

    ONLY WORKS FOR HALF_ADDER !
    """
    if not isinstance(n, int) and not isinstance(m, int):
      raise TypeError("Given arguments must be integers")
    if n < 0 or m < 0 :
      raise Exception("Given arguments must be positive or zero intergers")

    # dec to bin
    n = bin(n)[2:]
    n = (len(self.inputs_ids)//2-len(n))*"0" + n

    # dec to bin
    m = bin(m)[2:]
    m = (len(self.inputs_ids)//2-len(m))*"0" + m

    return int(self.evaluate(n + m), 2) # bin to dec



  def evaluateAdder(self, n : int, m : int) -> int :
    """
    Adds [n] to [m]

    ONLY WORKS FOR ADDER !
    """
    if not isinstance(n, int) and not isinstance(m, int):
      raise TypeError("Given arguments must be integers")
    if n < 0 or m < 0 :
      raise Exception("Given arguments must be positive or zero intergers")

    # dec to bin
    n = bin(n)[2:]
    n = (len(self.inputs_ids)//2-len(n))*"0" + n

    # dec to bin
    m = bin(m)[2:]
    m = (len(self.inputs_ids)//2-len(m))*"0" + m

    return int(self.evaluate(n + m + "0"), 2) # bin to dec



  def simplify(self) -> None:
    """
    Simplifies a bool_circ (example : !(!(x)) = (x))
    """
    g1 = self.copy()
    n = 0
    while (n < len(self.nodes_not_io_ids)) or (g1 != self):
      g1 = self.copy()
      self.simplify_node(self.nodes_not_io_ids[n])
      if g1 == self:
        n += 1
      else:
        n = 0



  def isCopyNode(self, id : int) -> bool:
    """
    Check if a node of id [id] is a copy node or not
    """
    return self.node_by_id(id).label == "" and self.node_by_id(id).indegree() == 1 and id in self.nodes_not_io_ids
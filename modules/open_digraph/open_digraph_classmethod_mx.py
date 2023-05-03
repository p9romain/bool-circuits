import random as rd
import re

class open_digraph_classmethod_mx:
  @classmethod
  def empty(cls) :
    """
    Creates the empty graph
    """
    return cls([],[],{}, "")



  @classmethod
  def random(cls, n : int, bound : int, inputs : int = 0, outputs : int = 0, desc : str = "", loop_free : bool = False, DAG : bool = False, oriented : bool = False, undirected : bool = False) :
    """
    Creates a graph randomly, with [n] nodes, [inputs] inputs, [outputs] outputs and can have loop, DAG, oriented or undirected. [bound] indicates the number maximal of edges between two nodes
    """
    if not isinstance(n, int):
        raise Exception("The number of nodes must be an integer")
    if n < 0 :
        raise Exception("The number of nodes must be positive or zero")
    if not isinstance(bound, int):
        raise Exception("The bound must be an integer")
    if bound <= 0 :
        raise Exception("The bound must be positive")
    if not isinstance(inputs, int):
        raise Exception("The inputs must be an integer")
    if inputs < 0 :
        raise Exception("The outputs must be positive or zero")
    if not isinstance(outputs, int):
        raise Exception("The inputs must be an integer")
    if outputs < 0 :

        raise Exception("The outputs must be positive or zero")
    if not isinstance(loop_free, bool):
        raise Exception("The loop_free must be a bool")
    if not isinstance(DAG, bool):
        raise Exception("The DAG must be a bool")
    if not isinstance(oriented, bool):
        raise Exception("The oriented must be a bool")
    if not isinstance(undirected, bool):
        raise Exception("The undirected must be a bool")

    if n == 0 : return cls.empty()

    # pour éviter les inclusions circulaires
    import modules.adjacency_matrix as am

    M = am.random_matrix(n, bound, null_diag = loop_free, oriented = oriented, triangular = DAG, symetric = undirected)
    cls = am.graph_from_adjacency_matrix(M)
    cls.desc = desc 

    if inputs > n or outputs > n :
        raise Exception("Can't have more inputs ou outputs than nodes in the graph")

    inputs = rd.sample(cls.nodes_ids, inputs)
    outputs = rd.sample(cls.nodes_ids, outputs)

    for l, i in enumerate(inputs):
        cls.add_input_node('i'+str(l), {i: 1})
    for l, i in enumerate(outputs):
        cls.add_output_node('o'+str(l), {i: 1})

    return cls



  @classmethod
  def from_dot_file(cls, path : str = "dot_files/graph.dot") :
    """
    Creates a graph from a .dot file
    """
    if not isinstance(path, str):
        raise Exception("The path must be a string")

    g = cls.empty()

    f = open(path, 'r')
    lines = f.readlines()
    for k in lines:
        l = k.rstrip('\n').strip()
        if l != "":
            regex_node = r'n([0-9]+) \[(.+)\][ ]*;'
            regex_edge = r'n([0-9]+)[ ]*->[ ]*n([0-9]+)[ ]*'
            
            res_node = re.findall(regex_node, l)
            if res_node:
                for node in res_node:
                    if len(node) == 2:
                        id = int(node[0])
                        list_attr = node[1].split(',')
                        attr = {}
                        for a in list_attr:
                            key,value = a.split('=')
                            attr[key] = value[1:-1]

                        if "label" in attr:
                            # fix verbose
                            if re.search(r'id:',attr["label"]):
                                attr["label"] = attr["label"].split('id')[0].strip().rstrip('\\n').strip()
                        else:
                            raise Exception("Line for node is not in the right format : missing attr called 'label'.")

                        s = attr["shape"] if "shape" in attr else ""

                        if s == "box":
                            g.add_input_node(attr["label"], id = id)
                        elif s == "diamond":
                            g.add_output_node(attr["label"], id = id)
                        else:
                            g.add_node(attr["label"], id = id)
                    else: raise Exception("Line for node is not in the right format : missing id or attr.")

            res_edge = re.findall(regex_edge, l)
            if res_edge:
                for edge in res_edge:
                    if len(edge) == 2:
                        id_p = int(edge[0])
                        id_c = int(edge[1])

                        g.add_edge((id_p, id_c))
                    else: raise Exception("Line for edge is not in the right format : missing src or dst")
    f.close()

    return g



  @classmethod
  def parallel(cls, g1, g2):
    """
    Creates a graph with [g1] in parallel of [g2]
    """
    g1_copy = g1.copy()
    g2_copy = g2.copy()
    g1_copy.iparallel(g2_copy)
    return g1_copy



  @classmethod
  def compose(cls, g1, g2):
    """
    Creates a graph [g1] composed with [g2].
    Graphs must have the same number of inputs and ouputs ([g2] comes after [g1])
    """
    g1_copy = g1.copy()
    g2_copy = g2.copy()
    g2_copy.icompose(g1_copy)
    return g2_copy
  


  @classmethod
  def identity(cls, n : int):
    """
    Creates the identity graph of size [n]
    It's [n] pairs of one input with one output
    """
    if not isinstance(n, int):
      raise TypeError("Given argument must be an int")

    g = cls.empty()
    
    for k in range(2*n):
      g.add_node()
    for k in range(n):
      g.add_edge((k,k+n))
        
    g.inputs_ids = list(range(n))
    g.outputs_ids = list(range(n,2*n))

    return g
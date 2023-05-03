import sys
import os
root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root) # allows us to fetch files from the project root

import random as rd
  
import modules.open_digraph.open_digraph as od
import modules.bool_circ.bool_circ as bc

class bool_circ_classmethod_mx(object):
  @classmethod
  def empty(cls) :
    """
    Creates the empty graph
    """
    return bc.bool_circ([],[],{}, "")



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

    char = ["&", "&&", "|", "||", "~", "!", "^", "0", "1", ""] # j'ai rajouté le nom de l'output qu'on avait oublié de préciser
    merge_list = {}

    for n in g.nodes_list :

      if not n.label in char and n.label != "" and n.label[0] != "o":
        if n.label in merge_list : merge_list[n.label] += [n.id]
        else: merge_list[n.label] = [n.id]

    for i in merge_list:
      if len(merge_list[i]) > 1:
        g.merge_nodes(merge_list[i])

      id_node = merge_list[i][0]
      g.node_by_id(id_node).label = ''
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
        g, _ = bool_circ_classmethod_mx.from_str("((a)&(b))|(((a)^(b))&(c))", "((a)^(b))^(c)")
        for o in g.outputs_list:
          o.label = ""
        for i in g.inputs_list:
          if i.label != "c":
            i.label = "" 
        return g
      else:
        # OLD CODE
        # g1 = bool_circ_classmethod_mx.adder(n-1)
        # g2 = g1.copy()

        # for i in g2.inputs_list:
        #   if i.label[0] == 'a': i.label = "A" + i.label[1:]
        #   elif i.label[0] == 'b': i.label = "B" + i.label[1:]
        #   elif i.label[0] == 'c': i.label = "C"

        # for i in g2.outputs_list:
        #   if i.label[0] == 'r': i.label = "R" + i.label[1:]
        #   elif i.label == "c'": i.label = "C'"

        # g = od.open_digraph.parallel(g1,g2)

        # g.display("dot_files/bool_circ/tmp1.dot", True)

        # # carry
        # n_C_prime = g.node_by_label(r"C'")[0]
        # n_c = g.node_by_label(r"^c$")[0]
        # g.add_edge((n_C_prime.parents_ids[0], n_c.children_ids[0]))
        # g.remove_node_by_id([n_C_prime.id,n_c.id])

        # g.display("dot_files/bool_circ/tmp2.dot", True)
        
        # # rename a_i with a_{n+i} and A_i with a_i
        # for i in g.node_by_label(r"[abr]+"):
        #   i.label = i.label[0] + str(int(i.label[1:])+n)
        # for i in g.node_by_label(r"[ABR]+"):
        #   i.label = i.label.lower()
        # g.node_by_label(r"C")[0].label = "c"








        # Logique du code :
        # g1 représente la partie du haut (donc avec le adder des bits les plus faible)
        # g2 représente la partie du bas (donc avec le adder des bits les plus forts)
        b = bis(n-1)

        g1 = od.open_digraph.parallel(od.open_digraph.identity(2**n), b)
        g2 = od.open_digraph.parallel(b, od.open_digraph.identity(2**(n-1)))

        # EXPLICATION (on veut a+b) :
        #
        # Les inputs de g1 resemble à ça :
        # [2^n de identity, 2^n de adder(n-1), 1 de carry]
        # donc à
        # [2^n de identity, 2^(n-1) de bits de a, 2^(n-1) de bits de b, 1 de carry]
        # En réalité dans la récusion, ça doit donner
        # [2^n de bit forts, 2^n de bits faibles, 1 de carry]
        #
        # Or dans la finalité, on va donner les inputs comme ceci :
        # [2^(n-1) de bit fort de a, 2^(n-1) de bit faible de a,2 ^(n-1) de bit fort de b, 2^(n-1) de bit faible de b, 1 de carry]
        # car on va donner a et b, dans cette ordre pour faire a+b
        #
        # et donc on échange bien pour avoir les bits faibles et forts ensemble
        for i in range(2**(n-1),2**n):
          tmp = g1.inputs_ids[i]
          g1.inputs_ids[i] = g1.inputs_ids[i+2**(n-1)]
          g1.inputs_ids[i+2**(n-1)] = tmp

        return od.open_digraph.compose(g1, g2)

    cls = bis(n)

    return cls
    


  @classmethod
  def half_adder(cls, n : int):
    cls = bool_circ_classmethod_mx.adder(n)
    node_c = cls.node_by_label(r"^c$")[0]
    cls.inputs_ids.remove(node_c.id)
    node_c.label = "0"
    return cls



  @classmethod
  def carry_lookahead(cls, n : int):
    def bis(n):
      if n == 0:
        def p(i): return f"(a{i})^(b{i})"
        def g(i): return f"(a{i})&(b{i})"
        def c(i): return "c" if i == 0 else f"({g(i-1)})^(({p(i-1)})&({c(i-1)}))"
        def o(i): return f"({p(i)})^({c(i)})"
        g, _ = bool_circ_classmethod_mx.from_str(o(0),o(1),o(2),o(3),o(4),g(n))
        for o in g.outputs_list:
          if int(o.label[1]) == 5: o.label = "c'"
          else: o.label = "r" + o.label[1] 
        return g
      else:
        g1 = bool_circ_classmethod_mx.carry_lookahead(0)
        g2 = bool_circ_classmethod_mx.carry_lookahead(n-1)

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
          i.label = i.label[0] + str(int(i.label[1:])+4*n)
        for i in g.node_by_label(r"[ABR]+"):
          i.label = i.label.lower()
        g.node_by_label(r"C")[0].label = "c"

        return g

    cls = bis(n)
    return cls



  @classmethod
  def from_int(cls, m : int, n : int = 8):
    """
    """
    if n == 0 or 2**n < m:
      raise Exception("Voilà, c'est tout.")

    s = bin(m)[2:]
    s = (n-len(s))*"0" + s
    cls = od.open_digraph.identity(n)
    for i in range(n):
      cls.inputs_ids.remove(i)
      cls.node_by_id(i).label = s[i]
    return cls
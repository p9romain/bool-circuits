import sys
import os
import re
root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root) # allows us to fetch files from the project root

from typing import List, Dict, Tuple
import random as rd
import numpy as np
import generic_heap as gh
import copy as cp

import modules.node as nd

class open_digraph: # for open directed graph
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

        # Tester s'ils sont corrects ?????
        # (genre conserver la bonne forme du graph)

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

        # Tester s'ils sont corrects ?????
        # (genre conserver la bonne forme du graph)

        self.__outputs_ids = o

    

    @desc.setter
    def desc(self, desc : str) -> None :
        """
        Setter for the description of the grph
        """
        if not isinstance(desc, str):
            raise Exception("The description must be a string")

        self.__desc = desc



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



    #pour les sets
    def __hash__(self) -> hash :
        return hash(self.desc*sys.getsizeof(self))

    

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

        # pour éviter les circular imports
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
        self.__nodes[n.id] = n
        
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
            for j in self.node_by_id(i).parent_ids:
                self.remove_parallel_edges((j, i))
                
            for j in self.node_by_id(i).children_ids:
                self.remove_parallel_edges((i, j))
                
            if i in self.inputs_ids: self.inputs_ids.remove(i)
            if i in self.outputs_ids: self.outputs_ids.remove(i)
            
            self.__nodes.pop(i)
        
        if isinstance(args, list) :
            types = set(type(k) for k in args)
            if len(types) >= 1 and list(types)[0] != int :
                raise TypeError("Elements in the given argument must all be integers")
            
            for arg in args.copy(): f(arg)

        elif isinstance(args, int) : 
            f(args)

        else:
            raise TypeError("Given argument must be a list of integers, or just one integer")



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
        b_outputs_ids_only_one_child = all(len(n.parent_ids) == 1 and n.parents[n.parent_ids[0]] == 1 for n in self.nodes_by_ids(self.outputs_ids).values())
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



    def save_as_dot_file(self, path : str = "dot_files/graph.dot", verbose : bool = False) -> None :
        """
        Saves the graph in a dot file
        The verbose adds the id in the file, not only the label of a node
        The add argument says if we add the graph at the end of the file
        """
        if not isinstance(path, str):
            raise Exception("The path must be a string")
        if not isinstance(verbose, bool):
            raise Exception("The verbose must be a bool")

        f = open(path, 'w')
        f.write("digraph G {\n")
        # nodes
        for n in self.nodes_list:
            attr = f"[label=\"{n.label}"
            if verbose:
                attr += f"\\n id: {n.id}"
            attr += "\""
            
            if n.id in self.inputs_ids:
                attr += ",shape=\"box\""
            if n.id in self.outputs_ids:
                attr += ",shape=\"diamond\""
            
            attr += "]"
            f.write(f"n{n.id} {attr};\n")
        #edges
        for a,b in self.edges:
            f.write(f"n{a} -> n{b}\n")
        f.write("}")
        f.close()



    def save_as_pdf_file(self, path : str = "dot_files/graph.dot", verbose : bool = False) -> str :
        """
        Saves the graph in a pdf file
        The verbose adds the id in the file, not only the label of a node
        The add argument says if we add the graph at the end of the file
        Returns the path of the pdf_file (useful for display)
        """
        if not isinstance(path, str):
            raise Exception("The path must be a string")
        if not isinstance(verbose, bool):
            raise Exception("The verbose must be a bool")

        n_path = (''.join(str(e)+"/" for e in path.split("/")[:-1]))+"output/"+(path.split("/")[-1].split(".")[0]+".pdf") 

        self.save_as_dot_file(path, verbose)
        os.system(f"dot -Tpdf \"{path}\" -Glabel=\"{self.desc}\" -o \"{n_path}\"")
        return n_path



    def display(self, path : str = "dot_files/graph.dot", verbose : bool = False) -> None :
        """
        Saves and display the graph in a pdf
        The verbose adds the id in the file, not only the label of a node
        """
        if not isinstance(path, str):
            raise Exception("The path must be a string")
        if not isinstance(verbose, bool):
            raise Exception("The verbose must be a bool")

        n_path = self.save_as_pdf_file(path, verbose)
        os.system(f"xdg-open \"{n_path}\"")



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



    def shift_indices(self, n : int) -> None :
        """
        Shifts all the ids of [n] (positive or negative)
        """
        if not isinstance(n, int):
            raise TypeError("Given argument must be an int")

        if self.min_id+n < 0: raise Exception("All the ids must be positive, even after the shift")

        def shift_indices_node(m):
            m.id += n
            m.parents = { k+n:v for (k,v) in m.parents.items() }
            m.children = { k+n:v for (k,v) in m.children.items() }
            return m

        self.__nodes = { k+n:shift_indices_node(v) for (k,v) in self.__nodes.items() }

        self.inputs_ids = [ i+n for i in self.inputs_ids ]
        self.outputs_ids = [ i+n for i in self.outputs_ids ]
    


    def iparallel(self, g) -> None :
        """
        Adds the graph [g] in parallel of [self]
        """
        g_copy = g.copy()
        g_copy.shift_indices(self.max_id-g_copy.min_id+1)
        
        self.desc = "Parallèle : " + self.desc + " & " + g_copy.desc
        self.__nodes.update(g_copy.nodes)
        self.inputs_ids += g_copy.inputs_ids
        self.outputs_ids += g_copy.outputs_ids
        
    

    @classmethod
    def parallel(cls, g1, g2):
        """
        Creates a graph with [g1] in parallel of [g2]
        """
        g1_copy = g1.copy()
        g2_copy = g2.copy()
        g1_copy.iparallel(g2_copy)
        return g1_copy
    


    def icompose(self, f) -> None:
        """
        Composes the graph [f] in [self].
        Graphs must have the same number of inputs and ouputs ([self] comes after [f])
        """
        if len(self.inputs_ids) != len(f.outputs_ids):
            raise Exception("Number of inputs and outputs don't match")
            
        f_copy = f.copy()
        f_copy.shift_indices(self.max_id-f_copy.min_id+1)
        self.__nodes.update(f_copy.nodes)
        
        for k,idk in enumerate(f_copy.outputs_ids):
            id_depart = self.node_by_id(idk).parent_ids[0]
            id_arrivee = self.node_by_id(self.inputs_ids[k]).children_ids[0]
            self.add_edge((id_depart,id_arrivee))
                
        self.remove_node_by_id(f_copy.outputs_ids)
        self.remove_node_by_id(self.inputs_ids)
        self.inputs_ids = f_copy.inputs_ids
    


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
     


    def connected_components(self):
        """
        Lists all the connected components of a graph. The dict looks like this :
        { node_id : 0, ..., node_id : 0, node_id : 1, ...., node_id : n }
        where 0, ..., n represents the id of the subgraph with nodes node_id, ..., node_id
        """
        comp = {}
        nodes_dict = self.nodes.copy()
        
        def pop_and_search(i, k):
            if i in nodes_dict:
                key_ids = set(list(nodes_dict.keys()))
                p_ids = nodes_dict[i].parent_ids
                p_ids = list(set(p_ids) & key_ids)
                c_ids = nodes_dict[i].children_ids
                c_ids = list(set(c_ids) & key_ids)
                del nodes_dict[i]
                comp[i] = k
                for t in p_ids: pop_and_search(t,k)
                for t in c_ids: pop_and_search(t,k)
        
        k = 0
        while len(nodes_dict) > 0:
            #ind = rd.choice(list(nodes_dict.keys())) (sûrement mieux mais pas possible pour les tests)
            ind = list(nodes_dict.keys())[0]
            pop_and_search(ind, k)
            k += 1
        
        return comp



    def connected_graphs(self):
        """
        Returns all the connected subgraphs in a list of graphs
        """
        comp = self.connected_components()
        l = []
        for k in list(set(comp.values())):
            nodes = [ self.node_by_id(i) for i, v in comp.items() if v == k ]
            inputs = [ i for i, v in comp.items() if v == k and i in self.inputs ]
            outputs = [ i for i, v in comp.items() if v == k and i in self.outputs ]
            l.append(open_digraph(inputs, outputs, nodes))
        return l 



    def dijkstra(self, src : int, direction : int = None, tgt : int = None) -> Tuple[Dict[int, int], Dict[int, int]] :
        """
        Returns the distace of all nodes from source node. Direction tells us to look only in the children's source node (1), parent's (-1) or both (None).
        Target node only look at path between src and tgt (can have several paths !!!)
        """
        if not isinstance(src, int):
            raise TypeError("Source node must be an integer (the id)")
        if direction != None and not isinstance(direction, int):
            raise TypeError("Direction must be an int")
        if direction != None and direction != -1 and direction != 1:
            raise Exception("Direction must be None, -1 or 1")

        if tgt != None and not isinstance(tgt, int):
            raise TypeError("Target node must be an integer (the id)")

        if not src in self.nodes_ids :
            raise Exception("Source node must be in the graph") 
        if tgt != None and not tgt in self.nodes_ids :
            raise Exception("Target node must be in the graph")

        Q = [ src ]
        dist = { src : 0 }
        prev = {}
        while Q != []:
            u = min(Q, key=(lambda x: dist[x]))
            Q.remove(u)
            if tgt != None and tgt == u : return dist, prev

            neighbours = []
            if direction == None or direction == -1 : neighbours += self.node_by_id(u).parent_ids
            if direction == None or direction == 1 : neighbours += self.node_by_id(u).children_ids
            for v in neighbours:
                if not v in dist : Q.append(v)
                if (not v in dist) or (dist[v] > dist[u] + 1):
                    dist[v] = dist[u] + 1
                    prev[v] = u
        return dist, prev



    def shortest_path(self, src : int, tgt : int) -> Dict[int, int] :
        """
        Returns the shortest path between [src] and [tgt] like this : { node : prec_node, [...] }
        """
        if not isinstance(src, int):
            raise TypeError("Source node must be an integer (the id)")
        if not isinstance(tgt, int):
            raise TypeError("Target node must be an integer (the id)")

        if src == tgt : return {}

        prev = self.dijkstra(src, None, tgt)[1]
        if not tgt in prev : 
            raise Exception("Target node must be accesible from source node (maybe your graph is oriented ?)")

        path = {}
        while tgt != src :
            path[tgt] = prev[tgt]
            tgt = prev[tgt]
        return path



    def common_ancestors(self, src : int, tgt : int) -> Dict[int, Tuple[int, int]] :
        """
        Returns the common ancestors with the distance from source and targer nodes { id_acestor : (dist from src, dist from tgt), [...] }
        """
        if not isinstance(src, int):
            raise TypeError("Source node must be an integer (the id)")
        if not isinstance(tgt, int):
            raise TypeError("Target node must be an integer (the id)")

        dist_src, prev_src = self.dijkstra(src, -1)
        dist_tgt, prev_tgt = self.dijkstra(tgt, -1)

        common_ancestors = list(set(prev_src.keys()).intersection(set(prev_tgt.keys())))

        return { n : (dist_src[n], dist_tgt[n]) for n in common_ancestors }
            

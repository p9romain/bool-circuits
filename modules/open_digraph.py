class node:
    def __init__(self, identity : int, label : str, parents : dict[int, int], children : dict[int, int]) -> None :
        '''
        identity: int; its unique id in the graph
        label: string;
        parents: int->int dict; maps a parent node's id to its multiplicity
        children: int->int dict; maps a child node's id to its multiplicity
        '''

        # Tests des cohérences de types, lol
        if not isinstance(identity, int):
            raise TypeError("The id must be an int")
        if not isinstance(label, str):
            raise TypeError("The label must be a string")

        # Test si c'est un dictionnaire
        if not isinstance(parents, dict):
            raise TypeError("Parents must be a dictionnary")
        types = set(type(k) for k in parents.keys()) # Crée l'ensemble des types dans les keys (donc pas de répétition)
        # Si c'est tous des entiers, le set n'a qu'une valeur : <class 'int'>
        # Sinon, c'est que c'est pas bon
        if len(types) >= 1 and list(types)[0] != int : # Teste si c'est pas un singeleton ou si son seul élément n'est pas int
            raise TypeError("The keys of parents must all be integers")
        types = set(type(k) for k in parents.values()) # Crée l'ensemble des types dans les values (donc pas de répétition)
        if len(types) >= 1 and list(types)[0] != int :
            raise TypeError("The values of parents must all be integers")


        if not isinstance(children, dict):
            raise TypeError("Children must be a dictionnary")
        types = set(type(k) for k in children.keys())
        if len(types) >= 1 and list(types)[0] != int :
            raise TypeError("The keys of children must all be integers")
        types = set(type(k) for k in children.values())
        if len(types) >= 1 and list(types)[0] != int :
            raise TypeError("The values of children must all be integers")

        self.__id = identity
        self.__label = label
        
        self.__parents = { p: m for (p, m) in parents.items() if m != 0 }
        self.__children = { c: m for (c, m) in children.items() if m != 0 }
        
    

    def copy(self):
        """
        Overload copy operator
        """
        return self.__init__(self.__id, self.__label, self.__parents, self.__children)
    
    

    @property
    def id(self) -> int :
        """
        Getter for the node's id
        """
        return self.__id
        
    

    @property
    def label(self) -> str :
        """
        Getter for the node's label
        """
        return self.__label
        
    

    @property
    def parent_ids(self) -> list[int] :
        """
        Getter for the ids of the node's parents
        """
        return list(self.__parents.keys())
        
    

    @property
    def children_ids(self) -> list[int] :
        """
        Getter for the ids of the node's children
        """
        return list(self.__children.keys())
    
    

    @property
    def parents(self) -> dict[int, int]:
        """
        Getter for the node's parents
        """
        return self.__parents
        
    

    @property
    def children(self) -> dict[int, int]:
        """
        Getter for the node's children
        """
        return self.__children
    
    

    @id.setter
    def id(self, i : int) -> None :
        """
        Setter for the node's id
        """
        if not isinstance(i, int):
            raise TypeError("Given argument must be an integer")

        self.__id = i
        
    

    @label.setter
    def label(self, l : str) -> None :
        """
        Setter for the node's label
        """
        if not isinstance(l, str):
            raise TypeError("Given argument must be a string")

        self.__label = l
        
    

    @parents.setter
    def parents(self, p : dict[int, int]) -> None :
        """
        Setter for the node's parents (erase all the attributes with the new dict)
        """
        if not isinstance(p, dict):
            raise TypeError("Given argument must be a dictionnary")
        types = set(type(k) for k in p.keys())
        if len(types) >= 1 and list(types)[0] != int :
            raise TypeError("The keys of the given argument must all be integers")
        types = set(type(k) for k in p.values())
        if len(types) >= 1 and list(types)[0] != int :
            raise TypeError("The values of the given argument must all be integers")

        self.__parents = p
        
    

    @children.setter
    def children(self, c : dict[int, int]) -> None :
        """
        Setter for the node's children (erase all the attributes with the new dict)
        """
        if not isinstance(c, dict):
            raise TypeError("Given argument must be a dictionnary")
        types = set(type(k) for k in c.keys())
        if len(types) >= 1 and list(types)[0] != int :
            raise TypeError("The keys of the given argument must all be integers")
        types = set(type(k) for k in c.values())
        if len(types) >= 1 and list(types)[0] != int :
            raise TypeError("The values of the given argument must all be integers")

        self.__children = c
        
    

    def __str__(self) -> str :
        """
        Overload str conversion
        """
        return f"[Node] (id = {self.__id}, label = {self.__label}, parents = {self.__parents}, children = {self.__children})"
        
    

    def __repr__(self) -> str :
        """
        Overload repr conversion (= str)
        """
        return self.__str__()

    

    def __eq__(self, other) -> bool :
        return (self.id == other.id) and (self.label == other.label) and (self.parents == other.parents) and (self.children == other.children)

    

    def __neq__(self, other) -> bool :
        return not self == other
        
    

    def add_child_id(self, i : int) -> None :
        """
        Adds the child of id [i] to the node : if it's already a child, add 1 to the multiplicity, else it just adds the child
        """
        if not isinstance(i, int):
            raise TypeError("Given argument must be an integer")

        if i in self.children:
            self.children[i] += 1
        else:
            self.children[i] = 1
            
    

    def add_parent_id(self, i : int) -> None :
        """
        Adds the parent of id [i] to the node : if it's already a parent, add 1 to the multiplicity, else it just adds the parent
        """
        if not isinstance(i, int):
            raise TypeError("Given argument must be an integer")

        if i in self.parents:
            self.parents[i] += 1
        else:
            self.parents[i] = 1
       
    

    def remove_parent_once(self, i : int) -> None :
        """
        Removes one to the multiplicity of the parent of id [i] : if it drops to 0, we get rid of it
        """
        if not isinstance(i, int):
            raise TypeError("Given argument must be an integer")
        
        if i in self.parent_ids:
            if self.parents[i] == 1: self.parents.pop(i)
            else: self.parents[i] -= 1
            
    

    def remove_parent_id(self, i : int) -> None :
        """
        Removes the parent of id [i]
        """
        if not isinstance(i, int):
            raise TypeError("Given argument must be an integer")
            
        if i in self.parent_ids: self.parents.pop(i)
        
    

    def remove_child_once(self, i : int) -> None :
        """
        Removes one to the multiplicity of the child of id [i] : if it drops to 0, we get rid of it
        """
        if not isinstance(i, int):
            raise TypeError("Given argument must be an integer")
        
        if i in self.children_ids:
            if self.children[i] == 1: self.children.pop(i)
            else: self.children[i] -= 1
            
    

    def remove_child_id(self, i: int) -> None :
        """
        Removes the child of id [i]
        """
        if not isinstance(i, int):
            raise TypeError("Given argument must be an integer")
            
        if i in self.children_ids: self.children.pop(i)
        
    
class open_digraph: # for open directed graph
    def __init__(self, inputs : list[int], outputs : list[int], nodes : iter) -> None:
        '''
        inputs: int list; the ids of the input nodes
        outputs: int list; the ids of the output nodes
        nodes: node iter;
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
        if len(types) >= 1 and list(types)[0] != node :
            raise TypeError("Elements in nodes must all be nodes")

        self.__inputs_ids = inputs
        self.__outputs_ids = outputs
        self.__nodes = {node.id:node for node in nodes} # self.nodes: <int,node> dict
        self.__new_id = (max(list(self.__nodes.keys())) + 1) if self.__nodes != {} else 0
 
    

    # can be useful maybe   
    @property
    def inputs(self) -> dict[int, node] :
        """
        Getter for the graph's inputs (a dict {note id: node})
        """
        return { i:self.__nodes[i] for i in self.__inputs_ids }

    

    # can be useful maybe
    @property
    def inputs_list(self) -> list[int] :
        """
        Getter for the graph's inputs
        """
        return [ self.__nodes[i] for i in self.__inputs_ids ]

    

    @property
    def inputs_ids(self) -> list[int] :
        """
        Getter for the graph's input's ids
        """
        return self.__inputs_ids

    

    # can be useful maybe    
    @property
    def outputs(self) -> dict[int, node] :
        """
        Getter for the graph's outputs (a dict {note id: node})
        """
        return { i:self.__nodes[i] for i in self.__outputs_ids }

    

    # can be useful maybe
    @property
    def outputs_list(self) -> list[int] :
        """
        Getter for the graph's outputs
        """
        return [ self.__nodes[i] for i in self.__outputs_ids ]

    

    @property
    def outputs_ids(self) -> list[int] :
        """
        Getter for the graph's output's ids
        """
        return self.__outputs_ids
    
    

    # id_nodes_map rename
    @property
    def nodes(self) -> dict[int, node] :
        """
        Getter for the graph's nodes (a dict {note id: node})
        """
        return self.__nodes
    
    

    # nodes rename
    @property
    def nodes_list(self) -> list[node] :
        """
        Getter for the graph's nodes
        """
        return list(self.nodes.values())
        
    

    @property
    def nodes_ids(self) -> list[int] :
        """
        Getter for the graph's nodes' id
        """
        return list(self.nodes.keys())
 
    

    @property
    def new_id(self) -> int :
        """
        Getter for an id which isn't in the graph
        """
        self.__new_id += 1
        return self.__new_id - 1

    

    @inputs_ids.setter
    def inputs_ids(self, i : list[int]) -> None :
        if not isinstance(i, list):
            raise TypeError("Given argument must be a list")
        types = set(type(k) for k in i)
        if len(types) >= 1 and list(types)[0] != int :
            raise TypeError("Elements in the given argument must all be integers")

        for k in i :
            if not k in self.nodes_ids:
                raise Exception("Given input isn't in the graph")

        self.__inputs_ids = i
        
    

    @outputs_ids.setter
    def outputs_ids(self, o : list[int]) -> None :
        if not isinstance(o, list):
            raise TypeError("Given argument must be a list")
        types = set(type(k) for k in o)
        if len(types) >= 1 and list(types)[0] != int :
            raise TypeError("Elements in the given argument must all be integers")

        for k in o :
            if not k in self.nodes_ids:
                raise Exception("Given output isn't in the graph")

        self.__outputs_ids = o

    

    def node_by_id(self, i : int) -> node :
        """
        ''Getter'' for the graph's node of id [i]
        """
        if not isinstance(i, int):
            raise TypeError("Given argument must be an integer")

        return self.nodes[i]
        
    

    def nodes_by_ids(self, l : list[int]) -> dict[int, node] :
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
    def empty(cls):
        """
        Creates the empty graph
        """
        return cls([],[],{})

    

    def add_node(self, label : str = '', parents : dict[int, int] = None, children : dict[int, int] = None) -> int :
        """
        Adds a node with given argument (label and its parents and children)
        It also generates all the edges bewteen the node and its 'family'
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

        n = node(self.new_id, label, {}, {})
        self.nodes[n.id] = n
        
        self.add_edge( [ (i, n.id) for i in parents.keys() for _ in range(parents[i]) ] )
        self.add_edge( [ (n.id, i) for i in children.keys() for _ in range(children[i]) ] )

        return n.id

    

    def add_input_node(self, label : str = '', children : dict[int, int] = None) -> int :
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

        nodeId = self.add_node(label, None, children)
        self.add_input_id(nodeId)
        return nodeId

    
    def add_output_node(self, label : str = '', parents : dict[int, int] = None) -> int :
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

        nodeId = self.add_node(label, parents, None)
        self.add_output_id(nodeId)
        return nodeId
    

    def add_edge(self, args : list[(int, int)] or (int, int)) -> None :
        """
        Adds one edge between one or several nodes' pair (src -> tgt)

        NON-ORIENTED GRAPH 
        """
        def f(src : int, tgt : int) -> None:
            if (not src in self.nodes_ids or not tgt in self.nodes_ids):
                raise Exception(f'The node with id {src} or {tgt} does not exist.')

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
          
    def remove_edge(self, args : list[(int, int)] or (int, int)) -> None :
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
    
       
    def remove_parallel_edges(self, args : list[(int, int)] or (int, int)) -> None :
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

    

    def remove_node_by_id(self, args : list[int] or int) -> None:
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
            
            self.nodes.pop(i)
            if i+1 == self.__new_id : 
                # -1 car on enlève le denier
                self.__new_id -= 1 
            # ici on utilise exceptionnellement pas le getter car comme il n'y a pas de setter, il faut accéder directement à l'attributs donc
            # autant y accéder de base + le fait qu'il aurait fallu décrément à chaque fois car le getter incrémente
        
        if isinstance(args, list) :
            types = set(type(k) for k in args)
            if len(types) >= 1 and list(types)[0] != int :
                raise TypeError("Elements in the given argument must all be integers")
            for arg in args: f(arg)

        elif isinstance(args, int) : 
            f(args)

        else:
            raise TypeError("Given argument must be a list of integers, or just one integer")

    

    def __str__(self) -> str :
        """
        Overload str conversion
        """
        V = [ v.label for v in self.nodes_list ]
        I = [ self.nodes[i].label for i in self.inputs_ids ]
        O = [ self.nodes[i].label for i in self.outputs_ids ]
        E = []
        for n in self.nodes_list:
            for key, value in n.children.items():
                for i in range(value):
                    E.append((n.label, self.nodes[key].label))
        return f"[Graph] (V = {V}, I = {I}, O = {O}, E = [{E}])"

    

    def __repr__(self) -> str :
        """
        Overload repr conversion (= str)
        """
        return self.__str__()
        
    

    def copy(self):
        """
        Overload copy operator
        """
        return self.__init__(self.inputs_ids, self.outputs_ids, self.nodes_list)
        
    

    def is_well_formed(self) -> bool :
        """
        Check if a graph is well formed :
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
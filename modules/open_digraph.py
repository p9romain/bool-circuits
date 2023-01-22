class node:
    def __init__(self, identity, label, parents, children):
        '''
        identity: int; its unique id in the graph
        label: string;
        parents: int->int dict; maps a parent node's id to its multiplicity
        children: int->int dict; maps a child node's id to its multiplicity
        '''

        # Tests des cohérences de types, lol
        if not isistance(identity, int):
            raise TypeError("The id must be an int")
        if not isistance(label, str):
            raise TypeError("The label must be a string")

        # Test si c'est un dictionnaire
        if not isistance(parents, dict):
            raise TypeError("Parents must be a dictionnary")
        types = set(type(k) for k in parents.keys()) # Crée l'ensemble des types dans les keys (donc pas de répétition)
        # Si c'est tous des entiers, le set n'a qu'une valeur : <class 'int'>
        # Sinon, c'est que c'est pas bon
        elif len(types) != 1 or next(iter(types)) != int : # Teste si c'est pas un singeleton ou si son seul élément n'est pas int
            raise TypeError("The keys of parents must all be integers")
        types = set(type(k) for k in parents.values())
        elif len(types) != 1 or next(iter(types)) != int :
            raise TypeError("The values of parents must all be integers")


        if not isistance(children, dict):
            raise TypeError("Children must be a dictionnary")
        types = set(type(k) for k in children.keys())
        elif len(types) != 1 or next(iter(types)) != int :
            raise TypeError("The keys of children must all be integers")
        types = set(type(k) for k in children.values())
        elif len(types) != 1 or next(iter(types)) != int :
            raise TypeError("The values of children must all be integers")

        self.__id = identity
        self.__label = label
        self.__parents = parents
        self.__children = children
        
    def __str__(self):
        return f"[Node] (id = {self.__id}, label = {self.__label}, parents = {self.__parents}, children = {self.__children})"
        
    def __repr__(self):
        return self.__str__()
        
    def copy(self):
        return self.__init__(self.__id, self.__label, self.__parents, self.__children)
    
    @property
    def id(self):
        return this.__id
        
    @property
    def label(self):
        return self.__label
        
    @property
    def parent_ids(self):
        return self.__parents.keys()
        
    @property
    def children_ids(self):
        return self.__children.keys()
        
    @id.setter
    def id(self, i):
        if not isistance(i, int):
            raise TypeError("Given argument must be an integer")

        self.__id = i
        
    @label.setter
    def label(self, l):
        if not isistance(i, str):
            raise TypeError("Given argument must be a string")

        self.__label = l
        
    @parents.setter
    def parents(self, p):
        if not isistance(p, dict):
            raise TypeError("Given argument must be a dictionnary")
        types = set(type(k) for k in p.keys())
        elif len(types) != 1 or next(iter(types)) != int :
            raise TypeError("The keys of the given argument must all be integers")
        types = set(type(k) for k in p.values())
        elif len(types) != 1 or next(iter(types)) != int :
            raise TypeError("The values of the given argument must all be integers")

        self.__parents = p
        
    @children.setter
    def children(self, c):
        if not isistance(c, dict):
            raise TypeError("Given argument must be a dictionnary")
        types = set(type(k) for k in c.keys())
        elif len(types) != 1 or next(iter(types)) != int :
            raise TypeError("The keys of the given argument must all be integers")
        types = set(type(k) for k in c.values())
        elif len(types) != 1 or next(iter(types)) != int :
            raise TypeError("The values of the given argument must all be integers")

        self.__children = c
        
    def add_child_id(self, i):
        if not isistance(i, int):
            raise TypeError("Given argument must be an integer")

        if i in self.__children:
            self.__children[i] += 1
        else:
            self.__children[i] = 1
            
    def add_parent_id(self, i):
        if not isistance(i, int):
            raise TypeError("Given argument must be an integer")

        if i in self.__parents:
            self.__parents[i] += 1
        else:
            self.__parents[i] = 1
    
class open_digraph: # for open directed graph
    def __init__(self, inputs, outputs, nodes):
        '''
        inputs: int list; the ids of the input nodes
        outputs: int list; the ids of the output nodes
        nodes: node iter;
        '''
        # Comme pour les dictionnaires plus haut
        if not isistance(inputs, list):
            raise TypeError("Inputs must be a list")
        types = set(type(k) for k in inputs)
        elif len(types) != 1 or next(iter(types)) != int :
            raise TypeError("Elements in inputs must all be integers")

        if not isistance(outputs, list):
            raise TypeError("Outputs must be a list")
        types = set(type(k) for k in outputs)
        elif len(types) != 1 or next(iter(types)) != int :
            raise TypeError("Elements in outputs must all be integers")

        # On teste si c'est un itérateur quelconque
        try:
           _ = (e for e in nodes) # oui oui cette syntaxe ne fonctionne qu'avec les itérateurs en fait
        except TypeError:
           raise TypeError("Nodes must be an iterator")
        # On teste si ça contient bien que des nodes
        types = set(type(k) for k in nodes)
        elif len(types) != 1 or next(iter(types)) != nodes :
            raise TypeError("Elements in nodes must all be nodes")

        self.__inputs = inputs
        self.__outputs = outputs
        self.__nodes = {node.id:node for node in nodes} # self.nodes: <int,node> dict
        self.__new_id = max(self.node_ids) + 1
    
    @property
    def input_ids(self):
        return self.__inputs
    
    @property
    def output_ids(self):
        return self.__outputs
    
    @property
    def id_node_map(self):
        return self.__nodes
    
    @property
    def nodes(self):
        return self.__nodes.values()
        
    @property
    def node_ids(self):
        return self.__nodes.keys()
        
    def node_by_id(self, i):
        if not isistance(i, int):
            raise TypeError("Given argument must be an integer")

        return self.__nodes[i]
        
    def nodes_by_ids(self, l):
        if not isistance(l, list):
            raise TypeError("Given argument must be a list")
        types = set(type(k) for k in inputs)
        elif len(types) != 1 or next(iter(types)) != int :
            raise TypeError("Elements in the given argument must all be integers")

        return { i:self.__nodes[i] for i in l }
    
    def add_input_id(self, i):
        if not isistance(i, int):
            raise TypeError("Given argument must be an integer")

        if not i in self.__inputs:
            self.__inputs.append(i)
            
    def add_output_id(self, i):
        if not isistance(i, int):
            raise TypeError("Given argument must be an integer")

        if not i in self.__outputs:
            self.__outputs.append(i)
    
    @inputs.setter
    def inputs(self, i):
        if not isistance(i, list):
            raise TypeError("Given argument must be a list")
        types = set(type(k) for k in i)
        elif len(types) != 1 or next(iter(types)) != int :
            raise TypeError("Elements in the given argument must all be integers")

        self.__inputs = i
        
    @outputs.setter
    def outputs(self, o):
        if not isistance(o, list):
            raise TypeError("Given argument must be a list")
        types = set(type(k) for k in o)
        elif len(types) != 1 or next(iter(types)) != int :
            raise TypeError("Elements in the given argument must all be integers")

        self.__outputs = o
    
    @classmethod
    def empty(cls):
        return cls([],[],{})

    @property
    def new_id(self):
        return self.__new_id

    def add_edge(self, src, tgt):
        if (not src in self.node_ids || not tgt in self.node_ids):
            raise Exception(f'The node with id {src} or {tgt} does not exist.')

        # non-orienté ? à demander
        self.node_by_id(src).add_child_id(tgt)
        self.node_by_id(tgt).add_child_id(src)

    def add_edges(self, edges):
        for (src, tgt) in edges:
            self.add_edge(src, tgt)

    def add_node(self, label = '', parents = None, children = None):
        for l in [parents, children]:
            if l is None: l = {}
            else:
                # par sécurité
                notin = list(set(l.keys()) - set(self.node_ids))
                for key in notin:
                    del l[key]
        n = node(self.__new_id, label, parents, children)
        self.__nodes[n.id] = n
        self.__new_id += 1

        return n.id

    def add_input_node(self, label = '', children = None):
        nodeId = self.add_node(label, None, children)
        self.add_input_id(nodeId)
        return nodeId

    def add_output_node(self, label = '', parents = None):
        nodeId = self.add_node(label, parents, None)
        self.add_output_id(nodeId)
        return nodeId

    def __str__(self):
        V = [ v.__label for v in self.__nodes.values() ]
        I = [ self.__nodes[i].label for i in self.__inputs ]
        O = [ self.__nodes[i].label for i in self.__outputs ]
        E = []
        for n in self.__nodes.values():
            for key, value in n.children.items():
                for i in range(value):
                    E.append((n.label, self.__nodes[key].label))
        return f"[Graph] (V = {V}, I = {I}, O = {O}, E = [{E}])"

    def __repr__(self):
        return self.__str__()
        
    def copy(self):
        return self.__init__(self.__inputs, self.__outputs, self.__nodes.values())

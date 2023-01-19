class node:
    def __init__(self, identity, label, parents, children):
        '''
        identity: int; its unique id in the graph
        label: string;
        parents: int->int dict; maps a parent node's id to its multiplicity
        children: int->int dict; maps a child node's id to its multiplicity
        '''
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
    def id(self, v):
        self.__id = v
        
    @label.setter
    def label(self, v):
        self.__label = v
        
    @parents.setter
    def parents(self, v):
        self.__parents = v
        
    @children.setter
    def children(self, v):
        self.__children = v
        
    def add_child_id(self, i):
        if i in self.__children:
            self.__children[i] += 1
        else:
            self.__children[i] = 1
            
    def add_parent_id(self, i):
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
        return self.__nodes[i]
        
    def nodes_by_ids(self, l):
        return { i:self.__nodes[i] for i in l }
    
    def add_input_id(self, i):
        if not i in self.__inputs:
            self.__inputs.append(i)
            
    def add_output_id(self, i):
        if not i in self.__outputs:
            self.__outputs.append(i)
    
    @inputs.setter
    def inputs(self, v):
        self.__inputs = v # tester la cohérence
        
    @outputs.setter
    def outputs(self, v):
        self.__outputs = v # tester la cohérence
    
    @classmethod
    def empty(cls):
        return cls([],[],{})

    @property
    def new_id(self):
        return self.__new_id

    def add_edge(self, src, tgt):
        if (not src in self.node_ids || not tgt in self.node_ids):
            raise Exception(f'The node with id {src} or {tgt} does not exist.')

        self.node_by_id(src).add_child_id(tgt)
        self.node_by_id(tgt).add_child_id(src)

    def add_edges(self, edges):
        for (src, tgt) in edges:
            self.add_edge(src, tgt)

    def add_node(self, label = '', parents = None, children = None):
        for l in [parents, children]:
            if l is None: l = {}
            else:
                # it's a security
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

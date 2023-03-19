from typing import List, Dict, Tuple, Set
import generic_heap as gh

class open_digraph_path_mx:
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



  def shortest_path(self, src : int, tgt : int) -> Tuple[int, Dict[int, int]] :
    """
    Returns the shortest path between [src] and [tgt] like this : { node : prec_node, [...] }
    """
    if not isinstance(src, int):
        raise TypeError("Source node must be an integer (the id)")
    if not isinstance(tgt, int):
        raise TypeError("Target node must be an integer (the id)")

    if src == tgt : return 0, {}

    dist, prev = self.dijkstra(src, None, tgt)
    if not tgt in prev : 
        raise Exception("Target node must be accesible from source node (maybe your graph is oriented ?)")

    path = {}
    while tgt != src :
        path[tgt] = prev[tgt]
        tgt = prev[tgt]
    return len(path), path



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
      
      
      
  def topologic_sort(self) -> List[Set[int]] :
    """
    Returns a topologic sort of the graph (list of sets with nodes ids). It works like this :
      [ l(0), l(1), ..., l(n) ] 
      - i < j => forall node u in l(i) and forall node v in l(j), u < v (where '<' is the order given by this sort)
      - forall u in l(i+1), exists v in l(i) s.t u is the child of v
    """
    g = self.copy()
    g.remove_node_by_id(g.outputs_ids + g.inputs_ids)
    heap = gh.Heap([ (n.indegree(), n.id) for n in g.nodes_list])

    res = []

    def bis(h):
        if h.empty(): return res
        else:
            s = set()
            while not h.empty() and h.peek()[0] == 0:
                s.add(h.peek()[1])
                g.remove_node_by_id(h.pop()[1])
            if not s and not g.empty(): raise Exception("The graph is cycli")
            res.append(s)
            h = gh.Heap([ (n.indegree(), n.id) for n in g.nodes_list])
            return bis(h)
    return bis(heap)


  def node_depth(self, id: int) -> int :
    """
    Returns the depth of a given node
    """
    if not isinstance(id, int):
        raise TypeError("Given argument must be an int")
        
    for i, li in enumerate(self.topologic_sort()):
        if id in li : return i
    raise Exception("Given node must be in the graph")
      
      
      
  def longest_path(self, src : int, tgt : int) -> Tuple[int, Dict[int, int]] :
    """
    Returns the longest path between [src] and [tgt] nodes
    """
    if not isinstance(src, int):
        raise TypeError("Source node must be an integer (the id)")
    if not isinstance(tgt, int):
        raise TypeError("Target node must be an integer (the id)")

    if not src in self.nodes_ids :
        raise Exception("Source node must be in the graph") 
    if not tgt in self.nodes_ids :
        raise Exception("Target node must be in the graph")
    
    l = self.topologic_sort()
    k_src = self.node_depth(src)
    k_tgt = self.node_depth(tgt)
    
    dist = { src : 0 }
    prev = {}
    
    for k in range(k_src+1, k_tgt+1):
        for w_id in l[k]:
            p_ids = self.node_by_id(w_id).parent_ids
            t = [ (i,dist[i]) for i in p_ids if i in dist ]
            if t:
                m_id, dist_max = max(t, key=(lambda x: x[1]))
                dist[w_id] = dist_max + 1
                prev[w_id] = m_id
    if prev == {} : return 0, {}
    
    path = {}
    while tgt != src :
        path[tgt] = prev[tgt]
        tgt = prev[tgt]
    return len(path), path
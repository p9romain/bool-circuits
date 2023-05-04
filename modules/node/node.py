import sys
import os
root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root) # allows us to fetch files from the project root

from typing import List, Dict
import copy as cp

import modules.node.node_add_remove_mx as nd_mx

class node(nd_mx.node_add_remove_mx):
  def __init__(self, id: int, label : str, parents : Dict[int, int], children : Dict[int, int]) -> None :
    '''
    identity: int; its unique id in the graph
    label: string;
    parents: int->int dict; maps a parent node's id to its multiplicity
    children: int->int dict; maps a child node's id to its multiplicity
    '''
    # Tests des cohérences de types, lol
    if not isinstance(id, int):
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

    self.__id = id
    self.__label = label
    
    self.__parents = { p: m for (p, m) in parents.items() if m != 0 }
    self.__children = { c: m for (c, m) in children.items() if m != 0 }
    


  def copy(self):
    """
    Overload copy operator
    """
    return cp.deepcopy(self)



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
  def parents_ids(self) -> List[int] :
    """
    Getter for the ids of the node's parents
    """
    return list(self.__parents.keys())
    


  @property
  def children_ids(self) -> List[int] :
    """
    Getter for the ids of the node's children
    """
    return list(self.__children.keys())



  @property
  def parents(self) -> Dict[int, int]:
    """
    Getter for the node's parents
    """
    return self.__parents
    


  @property
  def children(self) -> Dict[int, int]:
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
  def parents(self, p : Dict[int, int]) -> None :
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

    self.__parents = { p: m for (p, m) in p.items() if m != 0 }
      


  @children.setter
  def children(self, c : Dict[int, int]) -> None :
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

    self.__children = { c: m for (c, m) in c.items() if m != 0 }
    


  #pour les sets
  def __hash__(self) -> hash :
    """
    Setup the hash coding of a node
    """
    return hash(self.label*sys.getsizeof(self))



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
    """
    Overload eq operator
    """
    b1 = self.id == other.id
    b2 = self.label == other.label
    b3 = self.parents == other.parents
    b4 = self.children == other.children
    return b1 and b2 and b3 and b4



  def __neq__(self, other) -> bool :
    """
    Overload neq operator
    """
    return not self == other
    


  def indegree(self) -> int :
    """
    Returns the in-degree of the node
    """
    return sum(self.parents.values())



  def outdegree(self) -> int :
    """
    Returns the out-degree of the node
    """
    return sum(self.children.values())



  def degree(self) -> int :
    """
    Returns the degree of the node
    """
    return self.indegree()+self.outdegree()
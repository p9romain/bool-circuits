import sys
import os
root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root) # allows us to fetch files from the project root

from typing import List, Dict, Tuple
import numpy as np

import modules.open_digraph as od

def random_int_matrix(n : int, bound : int, null_diag : bool = False) -> np.ndarray :
    M = np.random.randint(0, bound+1, (n,n))
    if null_diag: return M - np.diag(M) * np.identity(n)
    else: return M



def random_symetric_int_matrix(n : int, bound : int, null_diag : bool = False) -> np.ndarray :
    M = random_int_matrix(n, bound, null_diag)
    return (M+M.T)/2



# j'enlève null_diag car oriented => null_diag (ça fait du taff en moins)
def random_oriented_int_matrix(n : int, bound : int) -> np.ndarray :
    M = random_int_matrix(n, bound, True)
    for i in range(n):
        for j in range(i+1, n):
            if M[i,j] != 0 and M[j,i] != 0:
                M[i,j] = 0
            # Echange
            b = np.random.randint(0, 2, 1)[0]
            if b:
                tmp = M[i,j]
                M[i,j] = M[j,i]
                M[j,i] = tmp
    return M



def random_triangular_int_matrix(n : int, bound : int, null_diag : bool = True) -> np.ndarray :
    return np.triu(random_int_matrix(n, bound, null_diag))



def random_matrix(n : int, bound : int, null_diag : bool = False, symetric : bool = False, oriented : bool = False, triangular : bool = False) -> np.ndarray :
    if symetric and oriented:
        raise Exception("The matrix of an oriented graph can't be symetric")
    elif symetric and triangular:
        raise Exception("A triangular matrix can'be symetric (exept null matrix and identity, but it's rare to get them with random)")
    
    # dans cet ordre, car triangular et oriented => triangular
    if symetric:
        return random_symetric_int_matrix(n, bound, null_diag)
    elif triangular:
        return random_triangular_int_matrix(n, bound, null_diag)
    elif oriented:
        return random_oriented_int_matrix(n, bound)
    else:
        return random_int_matrix(n, bound, null_diag)



def graph_from_adjacency_matrix(M : np.ndarray) -> od.open_digraph :
    g = od.open_digraph.empty()
    for i in range(M.shape[0]):
        g.add_node(label="n"+str(i))
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            g.add_edge([ (i,j) for _ in range(M[i,j]) ])
    return g
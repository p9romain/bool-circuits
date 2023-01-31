from typing import List, Dict, Tuple
import numpy as np

import open_digraph as od

def random_int_matrix(n, bound, null_diag=True):
    M = np.random.randint(0, bound+1, (n,n))
    if null_diag: return M - np.diag(M)@np.ones((n,n))
    else: return M

def random_symetric_int_matrix(n, bound, null_diag=True):
    M = random_int_matrix(n, bound, null_diag)
    return (M+M.T)/2

def random_oriented_int_matrix(n, bound, null_diag=True):
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

def random_triangular_int_matrix(n,bound,null_diag=True):
    return np.triu(random_int_matrix(n, bound, null_diag))

def random_matrix(n, bound, null_diag=False, symetric=False, oriented=False, triangular=False):
    if symetric and oriented:
        raise Exception("The matrix of an oriented graph can't be symetric")
    elif symetric and triangular:
        raise Exception("The only")
    
    if symetric:
        return random_symetric_int_matrix(n, bound, null_diag)
    elif triangular:
        return random_triangular_int_matrix(n, bound, null_diag)
    elif oriented:
        return random_oriented_int_matrix(n, bound, null_diag)
    else:
        return random_int_matrix(n, bound, null_diag)

def graph_from_adjacency_matrix(M):
    g = od.open_digraph.empty()
    for i in range(M.shape[0]):
        g.add_node(label="n"+str(i))
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            g.add_edge([ (i,j) for _ in range(M[i,j]) ])
    return g
import sys
import os
root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root) # allows us to fetch files from the project root
import unittest
import numpy as np

import modules.adjacency_matrix as am
import modules.open_digraph as od

class Adjacency_MAtrixTest(unittest.TestCase):
    def setUp(self):
        self.g0 = od.open_digraph.empty()

    def test_randomMatrixes(self):
        try:
            _ = am.random_matrix(5, 5, symetric = True, oriented = True)
        except Exception:
            self.assertEqual("", "")
        try:
            _ = am.random_matrix(2, 6, symetric = True, triangular = True)
        except Exception:
            self.assertEqual("", "")

        M = am.random_matrix(2, 6)
        self.assertEqual(M.shape, (2, 2))
        self.assertLessEqual(M.max(), 6)
        self.assertGreaterEqual(M.min(), 0)

        M = am.random_matrix(3, 2, null_diag = True)
        self.assertEqual(M.shape, (3, 3))
        self.assertLessEqual(M.max(), 2)
        self.assertGreaterEqual(M.min(), 0)
        self.assertEqual(list(np.diag(M)), 3*[0])

        M = am.random_matrix(2, 1, symetric = True)
        self.assertEqual(M.shape, (2, 2))
        self.assertLessEqual(M.max(), 1)
        self.assertGreaterEqual(M.min(), 0)
        self.assertEqual(M.T.tolist(), M.tolist())

        M = am.random_matrix(5, 6, null_diag = True, symetric = True)
        self.assertEqual(M.shape, (5, 5))
        self.assertLessEqual(M.max(), 6)
        self.assertGreaterEqual(M.min(), 0)
        self.assertEqual(list(np.diag(M)), 5*[0])
        self.assertEqual(M.T.tolist(), M.tolist())

        M = am.random_matrix(2, 5, triangular = True)
        self.assertEqual(M.shape, (2, 2))
        self.assertLessEqual(M.max(), 5)
        self.assertGreaterEqual(M.min(), 0)
        for i in range(M.shape[0]):
            for j in range(i):
                self.assertEqual(M[i][j], 0)


        M = am.random_matrix(3, 3, null_diag = True, triangular = True)
        self.assertEqual(M.shape, (3, 3))
        self.assertLessEqual(M.max(), 3)
        self.assertGreaterEqual(M.min(), 0)
        self.assertEqual(list(np.diag(M)), 3*[0])
        for i in range(M.shape[0]):
            for j in range(i):
                self.assertEqual(M[i][j], 0)


        M = am.random_matrix(3, 9, oriented = True)
        self.assertEqual(M.shape, (3, 3))
        self.assertLessEqual(M.max(), 9)
        self.assertGreaterEqual(M.min(), 0)
        for i in range(M.shape[0]):
            for j in range(M.shape[1]):
                if M[i][j] != 0 : self.assertEqual(M[j][i], 0)

        M = am.random_matrix(3, 2, null_diag = True, oriented = True)
        self.assertEqual(M.shape, (3, 3))
        self.assertLessEqual(M.max(), 2)
        self.assertGreaterEqual(M.min(), 0)
        self.assertEqual(list(np.diag(M)), 3*[0])
        for i in range(M.shape[0]):
            for j in range(M.shape[1]):
                if M[i][j] != 0 : self.assertEqual(M[j][i], 0)

    def test_adjacencyMatrix(self):
        self.g0 = od.open_digraph.empty()
        self.g0.add_input_node("i0")
        self.g0.add_input_node("i1")
        self.g0.add_output_node("o0")
        self.g0.add_node("n0")
        self.g0.add_node("n1")
        self.g0.add_node("n2")

        self.g0.add_edge([(3,5), (3,5), (3,4), (4, 3), (4,5),(0,3), (1,4), (5,2)])

        print("\n",self.g0,"\n")

        M = self.g0.adjacency_matrix()
        self.assertEqual(M.tolist(), [[0,1,2],[1,0,1],[0,0,0]])


    def test_graph(self):
        M = np.array([[0,1,2],[1,0,1],[0,0,0]])
        g = am.graph_from_adjacency_matrix(M)

        g.add_input_node("i0")
        g.add_input_node("i1")
        g.add_output_node("o0")

        g.add_edge([(3,0), (4,1), (2,5)])

        print("\n",g,"\n")

        #self.assertEqual(self.g0, g)

if __name__ == '__main__': # the following code is called only when
    unittest.main() # precisely this file is run

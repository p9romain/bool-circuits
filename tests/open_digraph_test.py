import sys
import os
root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root)# allows us to fetch files from the project root
import unittest
from modules.open_digraph import *

class NodeTest(unittest.TestCase):
    def setUp(self):
        self.n0 = node(0, 'i', {}, {1:1})
        
    def test_init(self):
        self.assertEqual(self.n0.id, 0)
        self.assertEqual(self.n0.label, 'i')
        self.assertEqual(self.n0.parents, {})
        self.assertEqual(self.n0.children, {1:1})
        self.assertIsInstance(self.n0, node)
        
    def test_copy(self):
        self.assertIsNot(self.n0.copy(), self.n0)

class Open_DigraphTest(unittest.TestCase):
    def setUp(self):
        n0 = node(0, 'a', {3:1, 4:1}, {1:1, 2:1})
        n1 = node(1, 'b', {0:1}, {2:2, 5:1})
        n2 = node(2, 'c', {0:1, 1:2}, {6:1})
        i0 = node(3, 'i0', {}, {0:1})
        i1 = node(4, 'i1', {}, {0:1})
        o0 = node(5, 'o0', {1:1}, {})
        o1 = node(6, 'o1', {2:1}, {})
        self.g0 = open_digraph([3,4], [5,6], [n0,n1,n2,i0,i1,o0,o1])
        
    def test_init(self):
        self.assertEqual(self.g0.inputs, [3,4])
        self.assertEqual(self.g0.outputs, [5,6])
        # need to overload eq operator
        #self.assertEqual(self.g0.nodes[0], node(0, 'a', {3:1, 4:1}, {1:1, 2:1}))
        self.assertIsInstance(self.g0, open_digraph)
        
    def test_empty(self):
        g = open_digraph.empty()
        self.assertEqual(g.inputs, [])
        self.assertEqual(g.outputs, [])
        self.assertEqual(g.nodes, {})
        
    def test_copy(self):
        self.assertIsNot(self.g0.copy(), self.g0)
        
            
if __name__ == '__main__': # the following code is called only when
    unittest.main() # precisely this file is run

import sys
import os
root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root) # allows us to fetch files from the project root
import unittest
import modules.node as nd

class NodeTest(unittest.TestCase):
    def setUp(self):
        self.n0 = nd.node(0, 'i', {}, {1:2})
        


    def test_init(self):
        # cf getters
        # self.assertEqual(self.n0.id, 0)
        # self.assertEqual(self.n0.label, 'i')
        # self.assertEqual(self.n0.parents, {})
        # self.assertEqual(self.n0.children, {1:2})

        self.assertIsInstance(self.n0, nd.node)
        self.assertEqual(str(self.n0), f"[Node] (id = 0, label = i, parents = { {} }, children = { {1:2} })")
        self.assertEqual(self.n0, nd.node(0, 'i', {}, {1:2}))
        


    def test_copy(self):
        self.assertIsNot(self.n0.copy(), self.n0)
        self.assertEqual(self.n0.copy(), self.n0)



    def test_getters(self):
        self.assertEqual(self.n0.id, 0)
        self.assertEqual(self.n0.label, 'i')
        self.assertEqual(self.n0.parent_ids, [])
        self.assertEqual(self.n0.children_ids, [1])
        self.assertEqual(self.n0.parents, {})
        self.assertEqual(self.n0.children, {1:2})



    def test_setters(self):
        n0 = self.n0.copy()

        n0.id = 4
        n0.label = "blouge"
        n0.parents = {1:3, 5:1, 4:1}
        n0.children = {7:29, 0:153, 2:0}

        self.assertEqual(n0.id, 4)
        self.assertEqual(n0.label, "blouge")
        self.assertEqual(n0.parents, {1:3, 5:1, 4:1})
        self.assertEqual(n0.children, {7:29, 0:153})



    def test_add(self):
        n0 = self.n0.copy()

        n0.add_parent_id(5)
        n0.add_child_id(1)

        self.assertEqual(n0.parent_ids, [5])
        self.assertEqual(list(n0.parents.values()), [1])
        self.assertEqual(n0.children_ids, [1])
        self.assertEqual(list(n0.children.values()), [3])



    def test_remove(self):
        n0 = self.n0.copy()

        n0.parents = {1:3, 5:1, 4:1}
        n0.children = {7:29, 0:153, 2:0}

        n0.remove_parent_once(5)
        n0.remove_child_once(7)

        n0.remove_parent_id(1)
        n0.remove_child_id(0)

        self.assertEqual(n0.parent_ids, [4])
        self.assertEqual(list(n0.parents.values()), [1])
        self.assertEqual(n0.children_ids, [7])
        self.assertEqual(list(n0.children.values()), [28])



    def test_degrees(self):
        n0 = self.n0.copy()

        self.assertEqual(n0.indegree(), 0)
        self.assertEqual(n0.outdegree(), 2)
        self.assertEqual(n0.degree(), 2)

        n0.parents = {1:3, 5:1, 4:1}
        n0.children = {7:29, 0:153, 2:0}

        self.assertEqual(n0.indegree(), 5)
        self.assertEqual(n0.outdegree(), 182)
        self.assertEqual(n0.degree(), 187)



if __name__ == '__main__': # the following code is called only when
    unittest.main() # precisely this file is run
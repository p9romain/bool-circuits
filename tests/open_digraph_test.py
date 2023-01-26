import sys
import os
root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root)# allows us to fetch files from the project root
import unittest
from modules.open_digraph import *

# class NodeTest(unittest.TestCase):
#     def setUp(self):
#         self.n0 = node(0, 'i', {}, {1:2})
        
#     def test_init(self):
#         self.assertEqual(self.n0.id, 0)
#         self.assertEqual(self.n0.label, 'i')
#         self.assertEqual(self.n0.parents, {})
#         self.assertEqual(self.n0.children, {1:2})
#         self.assertIsInstance(self.n0, node)
        
#     def test_copy(self):
#         self.assertIsNot(self.n0.copy(), self.n0)

#     def test_getters(self):
#         self.assertEqual(self.n0.id, 0)
#         self.assertEqual(self.n0.label, 'i')
#         self.assertEqual(self.n0.parent_ids, [])
#         self.assertEquel(self.n0.parents, [])
#         self.assertEqual(self.n0.child_ids, [1])
#         self.assertEquel(self.n0.children, [2])

#     def test_setters(self):
#         self.n0.id = 4
#         self.n0.label = "blouge"
#         self.n0.parents = {1:3, 5:1, 4:1}
#         self.n0.children = {7:29, 0:153, 2:0}

#         self.assertEqual(self.n0.id, 4)
#         self.assertEqual(self.n0.label, "blouge")
#         self.assertEqual(self.n0.parent_ids, [1, 5, 4])
#         self.assertEqual(self.n0.parents, [3, 1, 1])
#         self.assertEqual(self.n0.child_ids, [7, 0, 2])
#         self.assertEqual(self.n0.children, [29, 153, 0])

#         self.setUp()

#     def test_add(self):
#         self.add_child_id(1)
#         self.add_parent_id(5)

#         self.assertEqual(self.n0.parent_ids, [5])
#         self.assertEqual(self.n0.parents, [1])
#         self.assertEqual(self.n0.child_ids, [1])
#         self.assertEqual(self.n0.children, [3])
        
#         self.setUp()

#     def test_remove(self):
#         self.n0.set_parents_ids({1:3, 5:1, 4:1})
#         self.n0.set_children_ids({7:29, 0:153, 2:0})

#         self.remove_child_once(7)
#         self.remove_parent_once(5)

#         self.remove_child_id(0)
#         self.remove_parent_id(1)

#         self.assertEqual(self.n0.parent_ids, [1, 4])
#         self.assertEqual(self.n0.parents, [3, 1])
#         self.assertEqual(self.n0.child_ids, [7, 2])
#         self.assertEqual(self.n0.children, [28, 0])

#         self.setUp()


# class Open_DigraphTest(unittest.TestCase):
#     def setUp(self):
#         n0 = node(0, 'a', {3:1, 4:1}, {1:1, 2:1})
#         n1 = node(1, 'b', {0:1}, {2:2, 5:1})
#         n2 = node(2, 'c', {0:1, 1:2}, {6:1})
#         i0 = node(3, 'i0', {}, {0:1})
#         i1 = node(4, 'i1', {}, {0:1})
#         o0 = node(5, 'o0', {1:1}, {})
#         o1 = node(6, 'o1', {2:1}, {})
#         self.g0 = open_digraph([3,4], [5,6], [n0,n1,n2,i0,i1,o0,o1])
        
#     def test_init(self):
#         self.assertEqual(self.g0.inputs, [3,4])
#         self.assertEqual(self.g0.outputs, [5,6])
#         self.assertEqual(self.g0.nodes[0], node(0, 'a', {3:1, 4:1}, {1:1, 2:1}))
#         self.assertIsInstance(self.g0, open_digraph)
        
#     def test_empty(self):
#         g = open_digraph.empty()
#         self.assertEqual(g.inputs, [])
#         self.assertEqual(g.outputs, [])
#         self.assertEqual(g.nodes, {})
        
#     def test_copy(self):
#         self.assertIsNot(self.g0.copy(), self.g0)
        
#     def test_getters(self):
#         self.assertEqual(self.g0.input_ids, [3,4])
#         self.assertEqual(self.g0.output_ids, [5,6])
#         self.assertEqual(self.g0.id_node_map, {})
#         self.assertEqual(self.g0.nodes, 
#             [node(0, 'a', {3:1, 4:1}, {1:1, 2:1}),
#              node(1, 'b', {0:1}, {2:2, 5:1}),
#              node(2, 'c', {0:1, 1:2}, {6:1}),
#              node(3, 'i0', {}, {0:1}),
#              node(4, 'i1', {}, {0:1}),
#              node(5, 'o0', {1:1}, {}),
#              node(6, 'o1', {2:1}, {})
#              ])
#         self.assertEqual(self.g0.nodes_ids, [ i for i in range(7) ])
#         self.assertEqual(self.g0.get_node_by_id(4), node(4, 'i1', {}, {0:1}))
#         self.assertEqual(self.g0.get_nods_by_ids([1, 4, 0]), [node(1, 'b', {0:1}, {2:2, 5:1}), node(4, 'i1', {}, {0:1}), node(0, 'a', {3:1, 4:1}, {1:1, 2:1})])

#     # def test_setters(self):
#     #     self.g0.inputs = [1, 0, 5]
#     #     self.g0.outputs = []

#     #     self.assertEqual(self.g0.input_ids, [1, 0, 5])
#     #     self.assertEqual(self.g0.output_ids, [])

#     #     self.setUp()

#     def test_add(self):
#         self.g0.add_input_id(1)
#         self.g0.add_output_id(0)

#         self.assertEqual(self.g0.input_ids, [3, 4, 1])
#         self.assertEqual(self.g0.output_ids, [5, 6, 0])

#         self.setUp()

#         self.g0.add_edge(1, 3)
#         self.assertEqual(self.g0.nodes, 
#             [node(0, 'a', {3:1, 4:1}, {1:1, 2:1}),
#              node(1, 'b', {0:1}, {2:2, 5:1, 3:1}),
#              node(2, 'c', {0:1, 1:2}, {6:1}),
#              node(3, 'i0', {1: 1}, {0:1}),
#              node(4, 'i1', {}, {0:1}),
#              node(5, 'o0', {1:1}, {}),
#              node(6, 'o1', {2:1}, {})
#              ])

#         self.g0.add_edges([(0, 0), (1, 3), (1, 5)])
#         self.assertEqual(self.g0.nodes, 
#             [node(0, 'a', {3:1, 4:1, 0:1}, {1:1, 2:1, 0:1}),
#              node(1, 'b', {0:1}, {2:2, 5:2, 3:2}),
#              node(2, 'c', {0:1, 1:2}, {6:1}),
#              node(3, 'i0', {1: 2}, {0:1}),
#              node(4, 'i1', {}, {0:1}),
#              node(5, 'o0', {1:2}, {}),
#              node(6, 'o1', {2:1}, {})
#              ])

#         self.setUp()

#         x = self.g0.add_node()
#         self.assertEqual(x, 7)
#         x = self.g0.add_node(label = "d")
#         self.assertEqual(x, 8)
#         x = self.g0.add_node(parents = {1:2, 2:5})
#         self.assertEqual(x, 9)
#         x = self.g0.add_node(children = {1:1, 4:1})
#         self.assertEqual(x, 10)
#         x = self.g0.add_node("e", {3:1, 5:2, 0:1}, {2:4, 5:2})
#         self.assertEqual(x, 11)

#         self.assertEqual(self.g0.nodes, 
#             [node(0, 'a', {3:1, 4:1, 0:1}, {1:1, 2:1, 0:1, 11:1}),
#              node(1, 'b', {0:1, 10:1}, {2:2, 5:2, 3:2, 9:2}),
#              node(2, 'c', {0:1, 1:2, 11:4}, {6:1, 9:5}),
#              node(3, 'i0', {1: 2}, {0:1, 11:1}),
#              node(4, 'i1', {10:1}, {0:1}),
#              node(5, 'o0', {1:2, 11:2}, {11:2}),
#              node(6, 'o1', {2:1}, {}),
#              node(7, '', {}, {}),
#              node(8, 'd', {}, {}),
#              node(9, '', {1:2, 2:5}, {}),
#              node(10, '', {}, {1:1, 4:1}),
#              node(11, 'e', {3:1, 5:2, 0:1}, {2:4, 5:2})
#              ])

#         self.setUp()

#     def test_remove(self):
#         self.setUp()

#     def test_well_formed(self):
#         self.assertEqual(self.g0.is_well_formed(), True)
#         self.g0.assert_is_well_formed()


# if __name__ == '__main__': # the following code is called only when
#     unittest.main() # precisely this file is run

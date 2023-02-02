import sys
import os
root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root) # allows us to fetch files from the project root
import unittest
import modules.node as nd
import modules.open_digraph as od

class Open_DigraphTest(unittest.TestCase):
    def setUp(self):
        n0 = nd.node(0, 'a', {3:1, 4:1}, {1:3, 2:1})
        n1 = nd.node(1, 'b', {0:3}, {2:2, 5:1})
        n2 = nd.node(2, 'c', {0:1, 1:2}, {6:1})
        i0 = nd.node(3, 'i0', {}, {0:1})
        i1 = nd.node(4, 'i1', {}, {0:1})
        o0 = nd.node(5, 'o0', {1:1}, {})
        o1 = nd.node(6, 'o1', {2:1}, {})
        self.g0 = od.open_digraph([3,4], [5,6], [n0,n1,n2,i0,i1,o0,o1])
        
    def test_init(self):
        # cf getters
        # self.assertEqual(self.g0.inputs_ids, [3,4])
        # self.assertEqual(self.g0.outputs_ids, [5,6])
        # self.assertEqual(self.g0.nodes[0], node(0, 'a', {3:1, 4:1}, {1:1, 2:1}))

        self.assertIsInstance(self.g0, od.open_digraph)
        
    def test_empty(self):
        self.g0 = od.open_digraph.empty()
        self.assertEqual(self.g0.inputs_ids, [])
        self.assertEqual(self.g0.outputs_ids, [])
        self.assertEqual(self.g0.nodes, {})

        self.setUp()
        
    def test_copy(self):
        self.assertIsNot(self.g0.copy(), self.g0)
        
    def test_getters(self):
        self.assertEqual(self.g0.inputs,{ 3 : nd.node(3, 'i0', {}, {0:1}), 4 : nd.node(4, 'i1', {}, {0:1}) })
        self.assertEqual(self.g0.inputs_list, [ nd.node(3, 'i0', {}, {0:1}), nd.node(4, 'i1', {}, {0:1}) ])
        self.assertEqual(self.g0.inputs_ids, [3,4])

        self.assertEqual(self.g0.outputs, { 5 : nd.node(5, 'o0', {1:1}, {}), 6 : nd.node(6, 'o1', {2:1}, {}) } )
        self.assertEqual(self.g0.outputs_list, [ nd.node(5, 'o0', {1:1}, {}), nd.node(6, 'o1', {2:1}, {}) ])
        self.assertEqual(self.g0.outputs_ids, [5,6])

        self.assertEqual(self.g0.nodes_list, 
            [nd.node(0, 'a', {3:1, 4:1}, {1:3, 2:1}),
             nd.node(1, 'b', {0:3}, {2:2, 5:1}),
             nd.node(2, 'c', {0:1, 1:2}, {6:1}),
             nd.node(3, 'i0', {}, {0:1}),
             nd.node(4, 'i1', {}, {0:1}),
             nd.node(5, 'o0', {1:1}, {}),
             nd.node(6, 'o1', {2:1}, {})
             ])
        self.assertEqual(self.g0.nodes_ids, [ i for i in range(7) ])
        self.assertEqual(self.g0.node_by_id(4), nd.node(4, 'i1', {}, {0:1}))
        self.assertEqual(self.g0.nodes_by_ids([1, 4, 0]), { 1 : nd.node(1, 'b', {0:3}, {2:2, 5:1}), 4 : nd.node(4, 'i1', {}, {0:1}), 0 : nd.node(0, 'a', {3:1, 4:1}, {1:3, 2:1}) } )

        self.assertEqual(self.g0.new_id, 7)

        self.setUp() 
        # le getter new_id incrémente donc je remet tout à 0 pour la suite des tests

    def test_setters(self):
        self.g0.inputs_ids = [1, 0, 5]
        self.g0.outputs_ids = []

        self.assertEqual(self.g0.inputs_ids, [1, 0, 5])
        self.assertEqual(self.g0.outputs_ids, [])

        self.setUp()

    def test_add(self):
        self.g0.add_input_id(1)
        self.g0.add_output_id(0)

        self.assertEqual(self.g0.inputs_ids, [3, 4, 1])
        self.assertEqual(self.g0.outputs_ids, [5, 6, 0])

        self.setUp()

        self.g0.add_edge((1, 3))
        self.assertEqual(self.g0.nodes_list, 
            [nd.node(0, 'a', {3:1, 4:1}, {1:3, 2:1}),
             nd.node(1, 'b', {0:3}, {2:2, 5:1, 3:1}),
             nd.node(2, 'c', {0:1, 1:2}, {6:1}),
             nd.node(3, 'i0', {1: 1}, {0:1}),
             nd.node(4, 'i1', {}, {0:1}),
             nd.node(5, 'o0', {1:1}, {}),
             nd.node(6, 'o1', {2:1}, {})
             ])

        self.g0.add_edge([(0, 0), (1, 3), (1, 5)])
        self.g0.add_edge([])
        self.assertEqual(self.g0.nodes_list, 
            [nd.node(0, 'a', {3:1, 4:1, 0:1}, {1:3, 2:1, 0:1}),
             nd.node(1, 'b', {0:3}, {2:2, 5:2, 3:2}),
             nd.node(2, 'c', {0:1, 1:2}, {6:1}),
             nd.node(3, 'i0', {1: 2}, {0:1}),
             nd.node(4, 'i1', {}, {0:1}),
             nd.node(5, 'o0', {1:2}, {}),
             nd.node(6, 'o1', {2:1}, {})
             ])

        self.setUp()

        x = self.g0.add_node()
        self.assertEqual(x, 7)
        x = self.g0.add_node(label = "d")
        self.assertEqual(x, 8)
        x = self.g0.add_node(parents = {1:2, 2:5})
        self.assertEqual(x, 9)
        x = self.g0.add_node(children = {1:1, 4:1})
        self.assertEqual(x, 10)
        x = self.g0.add_node("e", {3:1, 5:2, 0:1}, {2:4, 5:2})
        self.assertEqual(x, 11)

        self.assertEqual(self.g0.nodes_list, 
            [nd.node(0, 'a', {3:1, 4:1}, {1:3, 2:1, 11:1}),
             nd.node(1, 'b', {0:3, 10:1}, {2:2, 5:1, 9:2}),
             nd.node(2, 'c', {0:1, 1:2, 11:4}, {6:1, 9:5}),
             nd.node(3, 'i0', {}, {0:1, 11:1}),
             nd.node(4, 'i1', {10:1}, {0:1}),
             nd.node(5, 'o0', {1:1, 11:2}, {11:2}),
             nd.node(6, 'o1', {2:1}, {}),
             nd.node(7, '', {}, {}),
             nd.node(8, 'd', {}, {}),
             nd.node(9, '', {1:2, 2:5}, {}),
             nd.node(10, '', {}, {1:1, 4:1}),
             nd.node(11, 'e', {3:1, 5:2, 0:1}, {2:4, 5:2})
             ])

        self.assertEqual(self.g0.new_id, 12)

        self.setUp()

        x = self.g0.add_input_node()
        self.assertEqual(x, 7)
        x = self.g0.add_input_node(label = "d")
        self.assertEqual(x, 8)
        x = self.g0.add_input_node(children = {})
        self.assertEqual(x, 9)
        x = self.g0.add_input_node("e", {2:1})
        self.assertEqual(x, 10)

        self.assertEqual(self.g0.nodes_list, 
            [nd.node(0, 'a', {3:1, 4:1}, {1:3, 2:1}),
             nd.node(1, 'b', {0:3}, {2:2, 5:1}),
             nd.node(2, 'c', {0:1, 1:2, 10:1}, {6:1}),
             nd.node(3, 'i0', {}, {0:1}),
             nd.node(4, 'i1', {}, {0:1}),
             nd.node(5, 'o0', {1:1}, {}),
             nd.node(6, 'o1', {2:1}, {}),
             nd.node(7, '', {}, {}),
             nd.node(8, 'd', {}, {}),
             nd.node(9, '', {}, {}),
             nd.node(10, 'e', {}, {2:1}),
             ])

        self.assertEqual(self.g0.new_id, 11)

        self.setUp()

        x = self.g0.add_output_node()
        self.assertEqual(x, 7)
        x = self.g0.add_output_node(label = "d")
        self.assertEqual(x, 8)
        x = self.g0.add_output_node(parents = {})
        self.assertEqual(x, 9)
        x = self.g0.add_output_node("e", {2:1})
        self.assertEqual(x, 10)

        self.assertEqual(self.g0.nodes_list, 
            [nd.node(0, 'a', {3:1, 4:1}, {1:3, 2:1}),
             nd.node(1, 'b', {0:3}, {2:2, 5:1}),
             nd.node(2, 'c', {0:1, 1:2}, {6:1, 10:1}),
             nd.node(3, 'i0', {}, {0:1}),
             nd.node(4, 'i1', {}, {0:1}),
             nd.node(5, 'o0', {1:1}, {}),
             nd.node(6, 'o1', {2:1}, {}),
             nd.node(7, '', {}, {}),
             nd.node(8, 'd', {}, {}),
             nd.node(9, '', {}, {}),
             nd.node(10, 'e', {2:1}, {}),
             ])

        self.assertEqual(self.g0.new_id, 11)

        self.setUp()

    def test_remove(self):
        self.g0.remove_edge((0, 2))
        self.g0.remove_edge([])
        self.g0.remove_edge([(0, 1), (4, 5)])

        self.g0.remove_parallel_edges((1,2))
        self.g0.remove_parallel_edges([])
        self.g0.remove_parallel_edges([(3, 0), (3,6)])

        self.assertEqual(self.g0.nodes_list, 
            [nd.node(0, 'a', {4:1}, {1:2}),
             nd.node(1, 'b', {0:2}, {5:1}),
             nd.node(2, 'c', {}, {6:1}),
             nd.node(3, 'i0', {}, {}),
             nd.node(4, 'i1', {}, {0:1}),
             nd.node(5, 'o0', {1:1}, {}),
             nd.node(6, 'o1', {2:1}, {})
             ])

        self.setUp()

        self.g0.remove_node_by_id(0)
        self.g0.remove_node_by_id([])
        self.g0.remove_node_by_id([3, 6])

        self.assertEqual(self.g0.nodes_list, 
            [nd.node(1, 'b', {}, {2:2, 5:1}),
             nd.node(2, 'c', {1:2}, {}),
             nd.node(4, 'i1', {}, {}),
             nd.node(5, 'o0', {1:1}, {})
             ])
        self.assertEqual(self.g0.new_id, 6)

        self.setUp()

    def test_well_formed(self):
        self.assertEqual(self.g0.is_well_formed(), True)
        self.g0.assert_is_well_formed()


if __name__ == '__main__': # the following code is called only when
    unittest.main() # precisely this file is run

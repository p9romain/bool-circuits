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
        self.g0 = od.open_digraph([3,4], [5,6], [n0,n1,n2,i0,i1,o0,o1], "graph_test")


        
    def test_init(self):
        # cf getters
        # self.assertEqual(self.g0.inputs_ids, [3,4])
        # self.assertEqual(self.g0.outputs_ids, [5,6])
        # self.assertEqual(self.g0.nodes[0], node(0, 'a', {3:1, 4:1}, {1:1, 2:1}))

        self.assertIsInstance(self.g0, od.open_digraph)
 


    def test_empty(self):
        g = od.open_digraph.empty()
        self.assertEqual(g.inputs_ids, [])
        self.assertEqual(g.outputs_ids, [])
        self.assertEqual(g.nodes, {})
        self.assertEqual(g.desc, "")
  


    def test_random(self):
        l = [ ("random", False, False, False, False), 
              ("random_loop_free", True, False, False, False), 
              ("random_undirected", False, False, False, True), 
              ("random_undirected_loop_free", True, False, False, True), 
              ("random_DAG", False, True, False, False), 
              ("random_DAG_loop_free", True, True, False, False), 
              ("random_oriented", False, False, True, False), 
              ("random_oriented_loop_free", True, False, True, False) ]

        for desc, loop_free, DAG, oriented, undirected in l :
            g = od.open_digraph.random(6, 3, 2, 2, desc, loop_free, DAG, oriented, undirected)
            g.save_as_pdf_file(path = f"dot_files/random/{desc}_graph.dot")



    def test_copy(self):
        self.assertIsNot(self.g0.copy(), self.g0)
        self.assertEqual(self.g0.copy(), self.g0)


        
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

        self.assertEqual(sorted(self.g0.edges, key = lambda a : a[0]), sorted([ (0, 1), (0, 1), (0, 1), (0, 2), (1, 2), (1, 2), (1, 5), (2, 6), (3, 0), (4, 0) ], key = lambda a : a[0]))

        self.assertEqual(self.g0.min_id, 0)
        self.assertEqual(self.g0.max_id, 6)

        self.assertEqual(self.g0.new_id, 7)

        self.assertEqual(self.g0.desc, "graph_test")

        self.setUp() 
        # le getter new_id incrémente donc je remet tout à 0 pour la suite des tests



    def test_setters(self):
        g = self.g0.copy()

        g.inputs_ids = [1, 0, 5]
        g.outputs_ids = []
        g.desc = "test"

        self.assertEqual(g.inputs_ids, [1, 0, 5])
        self.assertEqual(g.outputs_ids, [])
        self.assertEqual(g.desc, "test")


    def test_add(self):
        g = self.g0.copy()

        g.add_input_id(1)
        g.add_output_id(0)

        self.assertEqual(g.inputs_ids, [3, 4, 1])
        self.assertEqual(g.outputs_ids, [5, 6, 0])

        g = self.g0.copy()

        g.add_edge((1, 3))
        self.assertEqual(g.nodes_list, 
            [nd.node(0, 'a', {3:1, 4:1}, {1:3, 2:1}),
             nd.node(1, 'b', {0:3}, {2:2, 5:1, 3:1}),
             nd.node(2, 'c', {0:1, 1:2}, {6:1}),
             nd.node(3, 'i0', {1: 1}, {0:1}),
             nd.node(4, 'i1', {}, {0:1}),
             nd.node(5, 'o0', {1:1}, {}),
             nd.node(6, 'o1', {2:1}, {})
             ])

        g.add_edge([(0, 0), (1, 3), (1, 5)])
        g.add_edge([])
        self.assertEqual(g.nodes_list, 
            [nd.node(0, 'a', {3:1, 4:1, 0:1}, {1:3, 2:1, 0:1}),
             nd.node(1, 'b', {0:3}, {2:2, 5:2, 3:2}),
             nd.node(2, 'c', {0:1, 1:2}, {6:1}),
             nd.node(3, 'i0', {1: 2}, {0:1}),
             nd.node(4, 'i1', {}, {0:1}),
             nd.node(5, 'o0', {1:2}, {}),
             nd.node(6, 'o1', {2:1}, {})
             ])

        g = self.g0.copy()

        x = g.add_node()
        self.assertEqual(x, 7)
        x = g.add_node(label = "d")
        self.assertEqual(x, 8)
        x = g.add_node(parents = {1:2, 2:5})
        self.assertEqual(x, 9)
        x = g.add_node(children = {1:1, 4:1})
        self.assertEqual(x, 10)
        x = g.add_node("e", {3:1, 5:2, 0:1}, {2:4, 5:2})
        self.assertEqual(x, 11)

        self.assertEqual(g.nodes_list, 
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

        self.assertEqual(g.new_id, 12)

        g = self.g0.copy()

        x = g.add_input_node()
        self.assertEqual(x, 7)
        x = g.add_input_node(label = "d")
        self.assertEqual(x, 8)
        x = g.add_input_node(children = {})
        self.assertEqual(x, 9)
        x = g.add_input_node("e", {2:1})
        self.assertEqual(x, 10)

        self.assertEqual(g.nodes_list, 
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

        self.assertEqual(g.new_id, 11)

        g = self.g0.copy()

        x = g.add_output_node()
        self.assertEqual(x, 7)
        x = g.add_output_node(label = "d")
        self.assertEqual(x, 8)
        x = g.add_output_node(parents = {})
        self.assertEqual(x, 9)
        x = g.add_output_node("e", {2:1})
        self.assertEqual(x, 10)

        self.assertEqual(g.nodes_list, 
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

        self.assertEqual(g.new_id, 11)



    def test_remove(self):
        g = self.g0.copy()

        g.remove_edge((0, 2))
        g.remove_edge([])
        g.remove_edge([(0, 1), (4, 5)])

        g.remove_parallel_edges((1,2))
        g.remove_parallel_edges([])
        g.remove_parallel_edges([(3, 0), (3,6)])

        self.assertEqual(g.nodes_list, 
            [nd.node(0, 'a', {4:1}, {1:2}),
             nd.node(1, 'b', {0:2}, {5:1}),
             nd.node(2, 'c', {}, {6:1}),
             nd.node(3, 'i0', {}, {}),
             nd.node(4, 'i1', {}, {0:1}),
             nd.node(5, 'o0', {1:1}, {}),
             nd.node(6, 'o1', {2:1}, {})
             ])

        g = self.g0.copy()

        g.remove_node_by_id(0)
        g.remove_node_by_id([])
        g.remove_node_by_id([3, 6])

        self.assertEqual(g.nodes_list, 
            [nd.node(1, 'b', {}, {2:2, 5:1}),
            nd.node(2, 'c', {1:2}, {}),
            nd.node(4, 'i1', {}, {}),
            nd.node(5, 'o0', {1:1}, {})
            ])
        self.assertEqual(g.new_id, 6)

  

    def test_well_formed(self):
        self.assertEqual(self.g0.is_well_formed(), True)
        self.g0.assert_is_well_formed()

    

    def test_dot_to_graph(self):
        self.g0.save_as_dot_file("dot_files/graph_test_save_file.dot", True)
        g = od.open_digraph.from_dot_file("dot_files/graph_test_save_file.dot")
        self.assertEqual(self.g0, g)

        g = od.open_digraph.from_dot_file("dot_files/graph_test_save_file.dot")
        g.display("dot_files/graph_test_from_file_without_verbose.dot")

    

    def test_display(self):
        self.g0.display(verbose = True)



    def test_cyclic(self):
        self.assertEqual(self.g0.is_cyclic(), False)



    def test_shift_indices(self):
        g = self.g0.copy()
        g.shift_indices(20)
        self.assertEqual(g.nodes_ids, [ i + 20 for i in range(7) ])
        g.shift_indices(-20)
        self.assertEqual(self.g0, g)



if __name__ == '__main__': # the following code is called only when
    unittest.main() # precisely this file is run

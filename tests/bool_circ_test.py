import sys
import os
root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root) # allows us to fetch files from the project root
import unittest
import modules.node.node as nd
import modules.open_digraph.open_digraph as od
import modules.bool_circ as bc

class Bool_CircTest(unittest.TestCase):
    def setUp(self):
        i0 = nd.node(0, "i0", {}, {6:1})
        i1 = nd.node(1, "i1", {}, {7:1})
        o0 = nd.node(2, "o0", {8:1}, {})
        o1 = nd.node(3, "o1", {20:1}, {})

        c0 = nd.node(4, "0", {}, {8:1})
        c1 = nd.node(5, "1", {}, {11:1})

        n0 = nd.node(6, "", {0:1}, {8:1, 9:1})
        n1 = nd.node(7, "~", {1:1}, {10:1})
        n2 = nd.node(8, "||", {4:1, 6:1}, {2:1})
        n3 = nd.node(9, "~", {6:1}, {10:1})
        n4 = nd.node(10, "||", {9:1, 7:1}, {11:1})
        n5 = nd.node(11, "&&", {10:1, 5:1}, {12:1})
        n6 = nd.node(12, "", {11:1}, {13:1, 14:1})
        n7 = nd.node(13, "", {12:1}, {15:1, 16:1})
        n8 = nd.node(14, "~", {12:1}, {17:1})
        n9 = nd.node(15, "~", {13:1}, {18:1})
        n10 = nd.node(16, "", {13:1}, {18:1, 17:1})
        n11 = nd.node(17, "||", {16:1, 14:1}, {20:1})
        n12 = nd.node(18, "&&", {15:1, 16:1}, {19:1})
        n13 = nd.node(19, "", {18:1}, {20:2})
        n14 = nd.node(20, "&&", {19:2, 17:1}, {3:1})
        self.b0 = bc.bool_circ([0, 1], [2, 3], [i0, i1, o0, o1, c0, c1, n0, n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n13, n14], "bool_circ_test")



    def test_init(self):
        self.b0.save_as_pdf_file()
        self.b0.save_as_pdf_file("dot_files/bool_circ/bool_circ_verbose.dot", verbose=True)
        

    def test_from_str(self):
        b0, l0 = bc.bool_circ.from_str("((x0)&((x1)&(x2)))|((x1)&(~(x2)))")
        b0.save_as_pdf_file("dot_files/bool_circ/from_one_str.dot", True)
        self.assertEqual(l0, ['x0', 'x1', 'x2'])

        b1, l1 = bc.bool_circ.from_str("((x0)&((x1)&(x2)))|((x1)&(~(x2)))", "((x0)&(~(x1)))|(x2)")
        b1.save_as_pdf_file("dot_files/bool_circ/from_two_str.dot", True)
        self.assertEqual(l1, ['x0', 'x1', 'x2'])



    def test_random(self):
        b0 = bc.bool_circ.random(7, 1, 1, 2)
        b0.save_as_pdf_file("dot_files/bool_circ/random.dot")

    def test_adder(self):
        b0 = bc.bool_circ.adder(5)
        b0.display("dot_files/bool_circ/adder.dot", True)
        
if __name__ == '__main__': # the following code is called only when
    unittest.main() # precisely this file is run
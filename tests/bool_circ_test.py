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

        ###
        self.transforms_graph = {}

        n0 = nd.node(0, "0", {}, {1:1})
        n1 = nd.node(1, "", {0:1}, {2:1,3:1,4:1})
        c0 = nd.node(2, "o0", {1:1}, {})
        c1 = nd.node(3, "o1", {1:1}, {})
        c2 = nd.node(4, "o2", {1:1}, {})
        self.transforms_graph["copy"] = bc.bool_circ([], [2,3,4], [n0, n1, c0, c1, c2], "transform_copy")

        
        n0 = nd.node(0, "0", {}, {1:1})
        n1 = nd.node(1, "~", {0:1}, {2:1})
        c0 = nd.node(2, "o0", {1:1}, {})

        n2 = nd.node(3, "1", {}, {4:1})
        n3 = nd.node(4, "~", {3:1}, {5:1})
        c1 = nd.node(5, "o1", {4:1}, {})
        self.transforms_graph["not"] = bc.bool_circ([], [2,5], [n0, n1, c0, n2, n3, c1], "transform_not")


        a1 = nd.node(0, "&", {1:1,2:1,3:1}, {4:1})
        n1 = nd.node(1, "0", {}, {0:1})
        i1 = nd.node(2, "i1", {}, {0:1})
        i2 = nd.node(3, "i2", {}, {0:1})
        o1 = nd.node(4, "o1", {0:1}, {})


        a2 = nd.node(5, "&", {6:1,7:1,8:1}, {9:1})
        n2 = nd.node(6, "1", {}, {5:1})
        i3 = nd.node(7, "i1", {}, {5:1})
        i4 = nd.node(8, "i2", {}, {5:1})
        o2 = nd.node(9, "o1", {5:1}, {})

        self.transforms_graph["and"] = bc.bool_circ([2,3,7,8], [4,9], [a1,n1,i1,i2,o1,a2,n2,i3,i4,o2], "transform_and")
        

        a1 = nd.node(0, "|", {1:1,2:1,3:1}, {4:1})
        n1 = nd.node(1, "0", {}, {0:1})
        i1 = nd.node(2, "i1", {}, {0:1})
        i2 = nd.node(3, "i2", {}, {0:1})
        o1 = nd.node(4, "o1", {0:1}, {})


        a2 = nd.node(5, "|", {6:1,7:1,8:1}, {9:1})
        n2 = nd.node(6, "1", {}, {5:1})
        i3 = nd.node(7, "i1", {}, {5:1})
        i4 = nd.node(8, "i2", {}, {5:1})
        o2 = nd.node(9, "o1", {5:1}, {})

        self.transforms_graph["or"] = bc.bool_circ([2,3,7,8], [4,9], [a1,n1,i1,i2,o1,a2,n2,i3,i4,o2], "transform_or")
        

        a1 = nd.node(0, "^", {1:1,2:1,3:1}, {4:1})
        n1 = nd.node(1, "0", {}, {0:1})
        i1 = nd.node(2, "i1", {}, {0:1})
        i2 = nd.node(3, "i2", {}, {0:1})
        o1 = nd.node(4, "o1", {0:1}, {})


        a2 = nd.node(5, "^", {6:1,7:1,8:1}, {9:1})
        n2 = nd.node(6, "1", {}, {5:1})
        i3 = nd.node(7, "i1", {}, {5:1})
        i4 = nd.node(8, "i2", {}, {5:1})
        o2 = nd.node(9, "o1", {5:1}, {})

        self.transforms_graph["xor"] = bc.bool_circ([2,3,7,8], [4,9], [a1,n1,i1,i2,o1,a2,n2,i3,i4,o2], "transform_xor")
        

        n1 = nd.node(0, "|", {}, {1:1})
        o1 = nd.node(1, "o1", {0:1}, {})

        n2 = nd.node(2, "^", {}, {3:1})
        o2 = nd.node(3, "o2", {2:1}, {})
        
        n3 = nd.node(4, "&", {}, {5:1})
        o3 = nd.node(5, "o3", {4:1}, {})

        self.transforms_graph["neutral"] = bc.bool_circ([], [1,3,5], [n1,o1,n2,o2,n3,o3], "transform_neutral")
        

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
        b0 = bc.bool_circ.adder(2)
        b0.save_as_pdf_file("dot_files/bool_circ/adder.dot", True)



    def test_half_adder(self):
        b0 = bc.bool_circ.half_adder(2)
        b0.save_as_pdf_file("dot_files/bool_circ/half_adder.dot", True)



    def test_carry_lookahead(self):
        b0 = bc.bool_circ.carry_lookahead(2)
        b0.save_as_pdf_file("dot_files/bool_circ/carry_lookahead.dot", True)



    def test_from_int(self):
        b0 = bc.bool_circ.from_int(15, 9)
        b0.save_as_pdf_file("dot_files/bool_circ/from_int.dot", True)



    def test_transform_copy(self):
        self.transforms_graph["copy"].save_as_pdf_file("dot_files/bool_circ/transform/copy.dot", verbose=True)
        self.transforms_graph["copy"].transform_copy(1)
        self.transforms_graph["copy"].save_as_pdf_file("dot_files/bool_circ/transform/copy_done.dot", verbose=True)



    def test_transform_not(self):
        self.transforms_graph["not"].save_as_pdf_file("dot_files/bool_circ/transform/not.dot", verbose=True)
        self.transforms_graph["not"].transform_not(1)
        self.transforms_graph["not"].transform_not(4)
        self.transforms_graph["not"].save_as_pdf_file("dot_files/bool_circ/transform/not_done.dot", verbose=True)
    

    def test_transform_and(self):
        self.transforms_graph["and"].save_as_pdf_file("dot_files/bool_circ/transform/and.dot", verbose=True)
        self.transforms_graph["and"].transform_and(0)
        self.transforms_graph["and"].transform_and(5)
        self.transforms_graph["and"].save_as_pdf_file("dot_files/bool_circ/transform/and_done.dot", verbose=True)



    def test_transform_or(self):
        self.transforms_graph["or"].save_as_pdf_file("dot_files/bool_circ/transform/or.dot", verbose=True)
        self.transforms_graph["or"].transform_or(0)
        self.transforms_graph["or"].transform_or(5)
        self.transforms_graph["or"].save_as_pdf_file("dot_files/bool_circ/transform/or_done.dot", verbose=True)
    


    def test_transform_xor(self):
        self.transforms_graph["xor"].save_as_pdf_file("dot_files/bool_circ/transform/xor.dot", verbose=True)
        self.transforms_graph["xor"].transform_xor(0)
        self.transforms_graph["xor"].transform_xor(5)
        self.transforms_graph["xor"].save_as_pdf_file("dot_files/bool_circ/transform/xor_done.dot", verbose=True)



    def test_transform_neutral(self):
        self.transforms_graph["neutral"].save_as_pdf_file("dot_files/bool_circ/transform/neutral.dot", verbose=True)
        self.transforms_graph["neutral"].transform_neutral(0)
        self.transforms_graph["neutral"].transform_neutral(2)
        self.transforms_graph["neutral"].transform_neutral(4)
        self.transforms_graph["neutral"].save_as_pdf_file("dot_files/bool_circ/transform/neutral_done.dot", verbose=True)


    def test_transform(self):
        self.transforms_graph["copy"].transform(1)
        self.transforms_graph["copy"].save_as_pdf_file("dot_files/bool_circ/transform/copy_done_transform_fct.dot", verbose=True)
        
        self.transforms_graph["not"].transform(1)
        self.transforms_graph["not"].transform(4)
        self.transforms_graph["not"].save_as_pdf_file("dot_files/bool_circ/transform/not_done_transform_fct.dot", verbose=True)
    
        self.transforms_graph["and"].transform(0)
        self.transforms_graph["and"].transform(5)
        self.transforms_graph["and"].save_as_pdf_file("dot_files/bool_circ/transform/and_done_transform_fct.dot", verbose=True)

        self.transforms_graph["or"].transform(0)
        self.transforms_graph["or"].transform(5)
        self.transforms_graph["or"].save_as_pdf_file("dot_files/bool_circ/transform/or_done_transform_fct.dot", verbose=True)
    
        self.transforms_graph["xor"].transform(0)
        self.transforms_graph["xor"].transform(5)
        self.transforms_graph["xor"].save_as_pdf_file("dot_files/bool_circ/transform/xor_done_transform_fct.dot", verbose=True)

        self.transforms_graph["neutral"].transform(0)
        self.transforms_graph["neutral"].transform(2)
        self.transforms_graph["neutral"].transform(4)
        self.transforms_graph["neutral"].save_as_pdf_file("dot_files/bool_circ/transform/neutral_done_transform_fct.dot", verbose=True)


if __name__ == '__main__': # the following code is called only when
    unittest.main() # precisely this file is run
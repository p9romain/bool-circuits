import sys
import os
root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root) # allows us to fetch files from the project root
import unittest
import modules.node.node as nd
import modules.open_digraph.open_digraph as od
import modules.bool_circ.bool_circ as bc

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

        self.setUpTransform()
        self.setUpSimplify()



    def setUpTransform(self):
        self.transforms_graph = {}

        n0 = nd.node(0, "0", {}, {1:1})
        n1 = nd.node(1, "", {0:1}, {2:1, 3:1, 4:1})
        n2 = nd.node(2, "", {1:1}, {5:1})
        n3 = nd.node(3, "", {1:1}, {6:1})
        n4 = nd.node(4, "", {1:1}, {7:1})
        c0 = nd.node(5, "o0", {2:1}, {})
        c1 = nd.node(6, "o1", {3:1}, {})
        c2 = nd.node(7, "o2", {4:1}, {})
        self.transforms_graph["copy"] = bc.bool_circ([], [5,6,7], [n0, n1, n2, n3, n4, c0, c1, c2], "transform_copy")

        
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



    def setUpSimplify(self):
        self.simplify_graph = {}

        i0 = nd.node(0, "i0", {}, {4:1})
        i1 = nd.node(1, "i1", {}, {4:1})
        i2 = nd.node(2, "i2", {}, {5:1})
        i3 = nd.node(3, "i3", {}, {5:1})

        x1 = nd.node(4, "^", {0:1, 1:1}, {5:1})
        x2 = nd.node(5, "^", {4:1, 2:1, 3:1}, {6:1})

        o = nd.node(6, "o", {5:1}, {})

        self.simplify_graph["assoc_xor"] = bc.bool_circ([0, 1, 2, 3], [6], [i0, i1, i2, i3, x1, x2, o], "simplify_assoc_xor")


        i0 = nd.node(0, "i0", {}, {3:1})
        i1 = nd.node(1, "i1", {}, {3:1})
        i2 = nd.node(2, "i2", {}, {4:1})

        x = nd.node(3, "^", {0:1, 1:1, 4:1}, {5:1})
        c = nd.node(4, "", {2:1}, {3:1, 6:1, 7:1})

        o1 = nd.node(5, "o1", {3:1}, {})
        o2 = nd.node(6, "o2", {4:1}, {})
        o3 = nd.node(7, "o3", {4:1}, {})

        self.simplify_graph["invol_xor_1"] = bc.bool_circ([0, 1, 2], [5, 6, 7], [i0, i1, i2, x, c, o1, o2, o3], "simplify_invol_xor_1")

        i0 = nd.node(0, "i0", {}, {3:1})
        i1 = nd.node(1, "i1", {}, {3:1})
        i2 = nd.node(2, "i2", {}, {4:1})

        x = nd.node(3, "^", {0:1, 1:1, 4:2}, {5:1})
        c = nd.node(4, "", {2:1}, {3:2, 6:1, 7:1})

        o1 = nd.node(5, "o1", {3:1}, {})
        o2 = nd.node(6, "o2", {4:1}, {})
        o3 = nd.node(7, "o3", {4:1}, {})

        self.simplify_graph["invol_xor_2"] = bc.bool_circ([0, 1, 2], [5, 6, 7], [i0, i1, i2, x, c, o1, o2, o3], "simplify_invol_xor_2")

        i0 = nd.node(0, "i0", {}, {3:1})
        i1 = nd.node(1, "i1", {}, {3:1})
        i2 = nd.node(2, "i2", {}, {4:1})

        x = nd.node(3, "^", {0:1, 1:1, 4:3}, {5:1})
        c = nd.node(4, "", {2:1}, {3:3, 6:1, 7:1})

        o1 = nd.node(5, "o1", {3:1}, {})
        o2 = nd.node(6, "o2", {4:1}, {})
        o3 = nd.node(7, "o3", {4:1}, {})

        self.simplify_graph["invol_xor_3"] = bc.bool_circ([0, 1, 2], [5, 6, 7], [i0, i1, i2, x, c, o1, o2, o3], "simplify_invol_xor_3")


        i0 = nd.node(0, "i0", {}, {3:1})
        i1 = nd.node(1, "i1", {}, {3:1})
        i2 = nd.node(2, "i2", {}, {4:1})

        x = nd.node(3, "^", {0:1, 1:1, 4:1}, {5:1})
        n = nd.node(4, "!", {2:1}, {3:1})

        o = nd.node(5, "o", {3:1}, {})

        self.simplify_graph["not_xor"] = bc.bool_circ([0, 1, 2], [5], [i0, i1, i2, x, n, o], "simplify_not_xor")


        o0 = nd.node(0, "o0", {4:1}, {})
        o1 = nd.node(1, "o1", {4:1}, {})
        o2 = nd.node(2, "o2", {5:1}, {})
        o3 = nd.node(3, "o3", {5:1}, {})

        c1 = nd.node(4, "", {5:1}, {0:1, 1:1})
        c2 = nd.node(5, "", {6:1}, {4:1, 2:1, 3:1})

        i = nd.node(6, "i", {}, {5:1})

        self.simplify_graph["assoc_copy"] = bc.bool_circ([6], [0, 1, 2, 3], [o0, o1, o2, o3, c1, c2, i], "simplify_assoc_copy")


        i0 = nd.node(0, "i0", {}, {3:1})
        i1 = nd.node(1, "i1", {}, {3:1})
        i2 = nd.node(2, "i2", {}, {3:1})

        a = nd.node(3, "&&", {0:1, 1:1, 2:1}, {4:1})
        c = nd.node(4, "", {3:1}, {})

        self.simplify_graph["delete"] = bc.bool_circ([0, 1, 2], [], [i0, i1, i2, a, c], "simplify_delete")


        i = nd.node(0, "i", {}, {1:1})

        n = nd.node(1, "!", {0:1}, {2:1})
        c = nd.node(2, "", {1:1}, {3:1, 4:1, 5:1})

        o1 = nd.node(3, "o1", {2:1}, {})
        o2 = nd.node(4, "o2", {2:1}, {})
        o3 = nd.node(5, "o3", {2:1}, {})

        self.simplify_graph["not_copy"] = bc.bool_circ([0], [3, 4, 5], [i, n, c, o1, o2, o3], "simplify_not_copy")


        i = nd.node(0, "i", {}, {1:1})

        n1 = nd.node(1, "!", {0:1}, {2:1})
        n2 = nd.node(2, "!", {1:1}, {3:1,})

        o = nd.node(3, "o", {2:1}, {})

        self.simplify_graph["invol_not"] = bc.bool_circ([0], [3], [i, n1, n2, o], "simplify_invol_not")



    def test_init(self):
        self.b0.save_as_pdf_file()
        self.b0.save_as_pdf_file("dot_files/bool_circ/bool_circ_verbose.dot",)
        


    def test_from_str(self):
        b0, l0 = bc.bool_circ.from_str("((x0)&((x1)&(x2)))|((x1)&(~(x2)))")
        b0.save_as_pdf_file("dot_files/bool_circ/from_one_str.dot")
        self.assertEqual(l0, ['x0', 'x1', 'x2'])

        b1, l1 = bc.bool_circ.from_str("((x0)&((x1)&(x2)))|((x1)&(~(x2)))", "((x0)&(~(x1)))|(x2)")
        b1.save_as_pdf_file("dot_files/bool_circ/from_two_str.dot")
        self.assertEqual(l1, ['x0', 'x1', 'x2'])



    def test_random(self):
        b0 = bc.bool_circ.random(7, 1, 1, 2)
        b0.save_as_pdf_file("dot_files/bool_circ/random.dot")



    def test_adder(self):
        b0 = bc.bool_circ.adder(2)
        b0.save_as_pdf_file("dot_files/bool_circ/adder.dot")



    def test_half_adder(self):
        b0 = bc.bool_circ.half_adder(2)
        b0.save_as_pdf_file("dot_files/bool_circ/half_adder.dot")



    def test_carry_lookahead(self):
        b0 = bc.bool_circ.carry_lookahead(2)
        b0.save_as_pdf_file("dot_files/bool_circ/carry_lookahead.dot")



    def test_from_int(self):
        b0 = bc.bool_circ.from_int(15, 9)
        b0.save_as_pdf_file("dot_files/bool_circ/from_int.dot")



    def test_evaluate(self):
        b0, _ = bc.bool_circ.from_str("(!(x))||(!(x))")
        b0.save_as_pdf_file("dot_files/bool_circ/evaluate/not.dot")
        self.assertEqual(b0.evaluate(0), "1")
        self.assertEqual(b0.evaluate(1), "0")

        b0, _  = bc.bool_circ.from_str("(x)","(x)")
        b0.save_as_pdf_file("dot_files/bool_circ/evaluate/copy.dot")
        self.assertEqual(b0.evaluate(0), "00")
        self.assertEqual(b0.evaluate(1), "11")

        b0, _  = bc.bool_circ.from_str("((x1)&&(x2))")
        b0.save_as_pdf_file("dot_files/bool_circ/evaluate/and.dot")
        self.assertEqual(b0.evaluate("00"), "0")
        self.assertEqual(b0.evaluate("01"), "0")
        self.assertEqual(b0.evaluate("10"), "0")
        self.assertEqual(b0.evaluate("11"), "1")

        b0, _  = bc.bool_circ.from_str("((x1)||(x2))")
        b0.save_as_pdf_file("dot_files/bool_circ/evaluate/or.dot")
        self.assertEqual(b0.evaluate("00"), "0")
        self.assertEqual(b0.evaluate("01"), "1")
        self.assertEqual(b0.evaluate("10"), "1")
        self.assertEqual(b0.evaluate("11"), "1")

        b0, _  = bc.bool_circ.from_str("((x1)^(x2))")
        b0.save_as_pdf_file("dot_files/bool_circ/evaluate/xor.dot")
        self.assertEqual(b0.evaluate("00"), "0")
        self.assertEqual(b0.evaluate("01"), "1")
        self.assertEqual(b0.evaluate("10"), "1")
        self.assertEqual(b0.evaluate("11"), "0")

        self.assertEqual(self.b0.evaluate("01"), "00")
        self.assertEqual(self.b0.evaluate("10"), "10")



    def test_evaluate_adder(self):
        ad = bc.bool_circ.half_adder(2)
        self.assertEqual(ad.evaluate("01000110"), "01010") # 0100 + 0110 = 1010 (with carry 0)
        self.assertEqual(ad.evaluate("11000110"), "10010") # 1100 + 0110 = 10010 (with carry 1)

        ad = bc.bool_circ.half_adder(5)
        self.assertEqual(ad.evaluate("0100101100101110101001011010101001011010100111010000010110101101"), "010100101110010111010101101010111")
        # je te laisse vérifier sur internet ou manuellement

        self.assertEqual(ad.evaluateHalfAdder(1, 2), 3)
        self.assertEqual(ad.evaluateHalfAdder(1, 0), 1)
        self.assertEqual(ad.evaluateHalfAdder(0, 1), 1)
        self.assertEqual(ad.evaluateHalfAdder(15, 37), 52)
        self.assertEqual(ad.evaluateHalfAdder(2846423656, 23243), 2846446899)

        ad = bc.bool_circ.adder(5)
        self.assertEqual(ad.evaluateAdder(1, 2), 3)
        self.assertEqual(ad.evaluateAdder(1, 0), 1)
        self.assertEqual(ad.evaluateAdder(0, 1), 1)
        self.assertEqual(ad.evaluateAdder(15, 37), 52)
        self.assertEqual(ad.evaluateAdder(2846423656, 23243), 2846446899)



    def test_enc(self):
        b = bc.bool_circ.enc()
        b.save_as_pdf_file("dot_files/bool_circ/hamming/encoder.dot")



    def test_dec(self):
        b = bc.bool_circ.dec()
        b.save_as_pdf_file("dot_files/bool_circ/hamming/decoder.dot")



    def test_hamming(self):
        b_enc = bc.bool_circ.enc()
        b_dec = bc.bool_circ.dec()
        def f(i): # identity with not node on one
            b = od.open_digraph.identity(7) # because we just did for 4 -> 7 -> 4, so 7
            if i != -1 :
                b.add_node("~",{i:1},{i+7:1})
                b.remove_edge((i,i+7))
            return b

        def test_individual(b1, b2, b3, i): # enc + not node + dec
            b = od.open_digraph.compose(od.open_digraph.compose(b1, b2), b3)
            b.simplify()
            b.save_as_pdf_file(f"dot_files/bool_circ/hamming/encode_decode_with_one_errors_{i+1}.dot")
            for n in range(16):
                self.assertEqual(int(b.evaluate(n), 2), n) # try

        for i in range(-1, 7):
            test_individual(b_enc,f(i),b_dec, i)


        # with two not
        id = od.open_digraph.compose(f(1), f(3)) # two not nodes
        id = bc.bool_circ(id.inputs_ids, id.outputs_ids, id.nodes_list) # pour convertir en bool circ.......

        b = od.open_digraph.compose(od.open_digraph.compose(b_enc, id), b_dec)
        b.simplify()
        b.save_as_pdf_file("dot_files/bool_circ/hamming/encode_decode_with_two_errors.dot")

        for n in range(16):
            self.assertNotEqual(int(b.evaluate(n), 2), n) # try


# ------------------------- TRANSFORM -------------------------


    def test_transform_copy(self):
        self.setUpTransform() # pour reset

        self.transforms_graph["copy"].save_as_pdf_file("dot_files/bool_circ/transform/copy.dot",)
        self.transforms_graph["copy"].transform_copy(1)
        self.transforms_graph["copy"].transform_copy(2)
        self.transforms_graph["copy"].save_as_pdf_file("dot_files/bool_circ/transform/copy_done.dot",)



    def test_transform_not(self):
        self.setUpTransform() # pour reset

        self.transforms_graph["not"].save_as_pdf_file("dot_files/bool_circ/transform/not.dot",)
        self.transforms_graph["not"].transform_not(1)
        self.transforms_graph["not"].transform_not(4)
        self.transforms_graph["not"].save_as_pdf_file("dot_files/bool_circ/transform/not_done.dot",)
    
    

    def test_transform_and(self):
        self.setUpTransform() # pour reset

        self.transforms_graph["and"].save_as_pdf_file("dot_files/bool_circ/transform/and.dot",)
        self.transforms_graph["and"].transform_and(0)
        self.transforms_graph["and"].transform_and(5)
        self.transforms_graph["and"].save_as_pdf_file("dot_files/bool_circ/transform/and_done.dot",)



    def test_transform_or(self):
        self.setUpTransform() # pour reset

        self.transforms_graph["or"].save_as_pdf_file("dot_files/bool_circ/transform/or.dot",)
        self.transforms_graph["or"].transform_or(0)
        self.transforms_graph["or"].transform_or(5)
        self.transforms_graph["or"].save_as_pdf_file("dot_files/bool_circ/transform/or_done.dot",)
    


    def test_transform_xor(self):
        self.setUpTransform() # pour reset

        self.transforms_graph["xor"].save_as_pdf_file("dot_files/bool_circ/transform/xor.dot",)
        self.transforms_graph["xor"].transform_xor(0)
        self.transforms_graph["xor"].transform_xor(5)
        self.transforms_graph["xor"].save_as_pdf_file("dot_files/bool_circ/transform/xor_done.dot",)



    def test_transform_neutral(self):
        self.setUpTransform() # pour reset

        self.transforms_graph["neutral"].save_as_pdf_file("dot_files/bool_circ/transform/neutral.dot",)
        self.transforms_graph["neutral"].transform_neutral(0)
        self.transforms_graph["neutral"].transform_neutral(2)
        self.transforms_graph["neutral"].transform_neutral(4)
        self.transforms_graph["neutral"].save_as_pdf_file("dot_files/bool_circ/transform/neutral_done.dot",)



    def test_transform_node(self):
        self.setUpTransform() # pour reset

        self.transforms_graph["copy"].transform_node(1)
        self.transforms_graph["copy"].save_as_pdf_file("dot_files/bool_circ/transform/copy_done_transform_fct.dot",)
        
        self.transforms_graph["not"].transform_node(1)
        self.transforms_graph["not"].transform_node(4)
        self.transforms_graph["not"].save_as_pdf_file("dot_files/bool_circ/transform/not_done_transform_fct.dot",)
    
        self.transforms_graph["and"].transform_node(0)
        self.transforms_graph["and"].transform_node(5)
        self.transforms_graph["and"].save_as_pdf_file("dot_files/bool_circ/transform/and_done_transform_fct.dot",)

        self.transforms_graph["or"].transform_node(0)
        self.transforms_graph["or"].transform_node(5)
        self.transforms_graph["or"].save_as_pdf_file("dot_files/bool_circ/transform/or_done_transform_fct.dot",)
    
        self.transforms_graph["xor"].transform_node(0)
        self.transforms_graph["xor"].transform_node(5)
        self.transforms_graph["xor"].save_as_pdf_file("dot_files/bool_circ/transform/xor_done_transform_fct.dot",)

        self.transforms_graph["neutral"].transform_node(0)
        self.transforms_graph["neutral"].transform_node(2)
        self.transforms_graph["neutral"].transform_node(4)
        self.transforms_graph["neutral"].save_as_pdf_file("dot_files/bool_circ/transform/neutral_done_transform_fct.dot",)


# ------------------------- Simplify -------------------------


    def test_simplify_assoc_xor(self):
        self.setUpSimplify() # pour reset

        self.simplify_graph["assoc_xor"].save_as_pdf_file("dot_files/bool_circ/simplify/assoc_xor.dot")
        self.simplify_graph["assoc_xor"].simplify_assoc_xor(5)
        self.simplify_graph["assoc_xor"].save_as_pdf_file("dot_files/bool_circ/simplify/assoc_xor_done.dot")


    
    def test_simplify_invol_xor(self):
        self.setUpSimplify() # pour reset

        self.simplify_graph["invol_xor_1"].save_as_pdf_file("dot_files/bool_circ/simplify/invol_xor_1.dot")
        self.simplify_graph["invol_xor_1"].simplify_invol_xor(3)
        self.simplify_graph["invol_xor_1"].save_as_pdf_file("dot_files/bool_circ/simplify/invol_xor_1_done.dot")

        self.simplify_graph["invol_xor_2"].save_as_pdf_file("dot_files/bool_circ/simplify/invol_xor_2.dot")
        self.simplify_graph["invol_xor_2"].simplify_invol_xor(3)
        self.simplify_graph["invol_xor_2"].save_as_pdf_file("dot_files/bool_circ/simplify/invol_xor_2_done.dot")

        self.simplify_graph["invol_xor_3"].save_as_pdf_file("dot_files/bool_circ/simplify/invol_xor_3.dot")
        self.simplify_graph["invol_xor_3"].simplify_invol_xor(3)
        self.simplify_graph["invol_xor_3"].save_as_pdf_file("dot_files/bool_circ/simplify/invol_xor_3_done.dot")


    
    def test_simplify_not_xor(self):
        self.setUpSimplify() # pour reset

        self.simplify_graph["not_xor"].save_as_pdf_file("dot_files/bool_circ/simplify/not_xor.dot")
        self.simplify_graph["not_xor"].simplify_not_through_xor(3)
        self.simplify_graph["not_xor"].save_as_pdf_file("dot_files/bool_circ/simplify/not_xor_done.dot")


    
    def test_simplify_assoc_copy(self):
        self.setUpSimplify() # pour reset

        self.simplify_graph["assoc_copy"].save_as_pdf_file("dot_files/bool_circ/simplify/assoc_copy.dot")
        self.simplify_graph["assoc_copy"].simplify_assoc_copy(5)
        self.simplify_graph["assoc_copy"].save_as_pdf_file("dot_files/bool_circ/simplify/assoc_copy_done.dot")


    
    def test_simplify_delete(self):
        self.setUpSimplify() # pour reset

        self.simplify_graph["delete"].save_as_pdf_file("dot_files/bool_circ/simplify/delete.dot")
        self.simplify_graph["delete"].simplify_delete(3)
        self.simplify_graph["delete"].save_as_pdf_file("dot_files/bool_circ/simplify/delete_done.dot")


    
    def test_simplify_not_copy(self):
        self.setUpSimplify() # pour reset

        self.simplify_graph["not_copy"].save_as_pdf_file("dot_files/bool_circ/simplify/not_copy.dot")
        self.simplify_graph["not_copy"].simplify_not_through_copy(2)
        self.simplify_graph["not_copy"].save_as_pdf_file("dot_files/bool_circ/simplify/not_copy_done.dot")


    
    def test_simplify_not_not(self):
        self.setUpSimplify() # pour reset

        self.simplify_graph["invol_not"].save_as_pdf_file("dot_files/bool_circ/simplify/invol_not.dot")
        self.simplify_graph["invol_not"].simplify_invol_not(1)
        self.simplify_graph["invol_not"].save_as_pdf_file("dot_files/bool_circ/simplify/invol_not_done.dot")


    
    def test_simplify_node(self):
        self.setUpSimplify() # pour reset

        self.simplify_graph["assoc_xor"].simplify_node(5)
        self.simplify_graph["assoc_xor"].save_as_pdf_file("dot_files/bool_circ/simplify/assoc_xor_done_simplify_fct.dot")


        self.simplify_graph["invol_xor_1"].simplify_node(3)
        self.simplify_graph["invol_xor_1"].save_as_pdf_file("dot_files/bool_circ/simplify/invol_xor_1_done_simplify_fct.dot")
        self.simplify_graph["invol_xor_2"].simplify_node(3)
        self.simplify_graph["invol_xor_2"].save_as_pdf_file("dot_files/bool_circ/simplify/invol_xor_2_done_simplify_fct.dot")
        self.simplify_graph["invol_xor_3"].simplify_node(3)
        self.simplify_graph["invol_xor_3"].save_as_pdf_file("dot_files/bool_circ/simplify/invol_xor_3_done_simplify_fct.dot")


        self.simplify_graph["not_xor"].simplify_node(3)
        self.simplify_graph["not_xor"].save_as_pdf_file("dot_files/bool_circ/simplify/not_xor_done_simplify_fct.dot")


        self.simplify_graph["assoc_copy"].simplify_node(5)
        self.simplify_graph["assoc_copy"].save_as_pdf_file("dot_files/bool_circ/simplify/assoc_copy_done_simplify_fct.dot")

        
        self.simplify_graph["delete"].simplify_node(3)
        self.simplify_graph["delete"].save_as_pdf_file("dot_files/bool_circ/simplify/delete_done_simplify_fct.dot")


        self.simplify_graph["not_copy"].simplify_node(2)
        self.simplify_graph["not_copy"].save_as_pdf_file("dot_files/bool_circ/simplify/not_copy_done_simplify_fct.dot")


        self.simplify_graph["invol_not"].simplify_node(1)
        self.simplify_graph["invol_not"].save_as_pdf_file("dot_files/bool_circ/simplify/invol_not_done_simplify_fct.dot")



if __name__ == '__main__': # the following code is called only when
    unittest.main() # precisely this file is run
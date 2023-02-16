import sys
import os
root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root) # allows us to fetch files from the project root
import unittest
import modules.bool_circ as bc

class Bool_CircTest(unittest.TestCase):
    def setUp(self):
        pass
        

        
    def test_init(self):
        pass



if __name__ == '__main__': # the following code is called only when
    unittest.main() # precisely this file is run
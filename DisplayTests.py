from Display import *
from ShameAndObedienceGameBoardTestVariables import *
import unittest

class DisplayGameboardMethodsTest(unittest.TestCase):

    def test_DisplayGameBoard_DemonstrateRunLoop(self):
        # uncomment below to run this test        
        gb = ShameAndObedienceGameBoardTestVariables.sample_gameboard2(assignElementsToRegion=("fit", 5))
        print("LOADING GAMEBOARD")
        dg = DisplayGameboard(gb)
        dg.init_screen()
        dg.run_loop()        

# finish this
# go back and work on scan algorithm.
if __name__ == "__main__":
    unittest.main()
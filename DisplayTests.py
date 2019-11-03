from Display import *
from ShameAndObedienceGameBoardTests import *
import unittest

class DisplayMethodsTest(unittest.TestCase):

    def test_demonstrate_run(self):
        gb = ShameAndObedienceGameBoardMethodsTest.sample_gameboard2()
        print("LOADING GAMEBOARD")
        dg = DisplayGameboard(gb)
        dg.run_loop()
        return


if __name__ == "__main__":
    unittest.main()

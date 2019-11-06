from Display import *
from ShameAndObedienceGameBoardTestVariables import *
import unittest

class DisplayGameboardMethodsTest(unittest.TestCase):

    def test_DisplayGameBoard_AssertCorrectInit(self):
        # uncomment below to run this test
        """
        gb = ShameAndObedienceGameBoardMethodsTest.sample_gameboard2()
        print("LOADING GAMEBOARD")
        dg = DisplayGameboard(gb)
        dg.init_screen()
        dg.run_loop()
        """
        return -1

    def test_DisplayGameBoard_BlankScoreboardBlankGameboardTests(self):

        gb = ShameAndObedienceGameBoardTestVariables.sample_gameboard2(("t/e",1))
        print("LOADING GAMEBOARD")
        dg = DisplayGameboard(gb)
        dg.init_screen()
        dg.run_loop()

        return -1


    def test_demonstrate_run(self):
        """
        gb = ShameAndObedienceGameBoardMethodsTest.sample_gameboard2()
        print("LOADING GAMEBOARD")
        dg = DisplayGameboard(gb)
        dg.run_loop()
        """
        return


# finish this
# go back and work on scan algorithm.


if __name__ == "__main__":
    unittest.main()

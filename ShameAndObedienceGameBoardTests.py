from ShameAndObedienceGameBoard import *
import unittest

class ShameAndObedienceGameBoardMethodsTest(unittest.TestCase):

    # TODO : refactor duplicate
    @staticmethod
    def sample_gameboard1():
        # get languages with random centroids of uniform size
        languageInfo = []
        dim = (8,8)
        for i in range(5):
            languageInfo.append(Language.random(idn = i, mode = "const"))
        q = ShameAndObedienceGameBoard(languageInfo, dim, 11)
        return q

    def setUp(self):
        self.gb = ShameAndObedienceGameBoardMethodsTest.sample_gameboard1()

    def test_ShameAndObedienceGameBoard_PaintGameBoard(self):
        self.gb.paint_elements()
        #print("AREADIFF :\t", self.gb.configAreaDiff)

if __name__ == "__main__":
    unittest.main()

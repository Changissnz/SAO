from GameBoard import *
import unittest
from time import time

class GameBoardMethodsTest(unittest.TestCase):

    @staticmethod
    def sample_gameboard1():
        # get languages with random centroids of uniform size
        languageInfo = []
        dim = (8,8)
        for i in range(5):
            languageInfo.append(Language.random(idn = i, mode = "const"))
        q = GameBoard(languageInfo, dim)
        return q
        """
        # print out element info
        print("gb language count :\t", self.gb.elementLanguageCount)
        print("gb language count :\t", self.gb.elementLanguageRatio)
        return -1
        """

    @staticmethod
    def sample_gameboard2():

        """
        def random(idn = "numero-unetas", languageFormation = "centroid",\
            minSizeInfo = 100, startSizeInfo = 5, mode = "geq"):
        """
        sizesInfo = [(400, 10), (2000, 30), (1000, 20)]
        languageInfo = []
        dim = (8,8)
        for i, s in enumerate(sizesInfo):
            languageInfo.append(Language.random(idn = i,\
                minSizeInfo = s[0], startSizeInfo = s[1], mode = "const"))
        return GameBoard(languageInfo, dim)

    def setUp(self):
        ##self.gb = GameBoardMethodsTest.sample_gameboard2()
        return -1

    # TODO : test areaDiff
    def test_GameBoard_AssignElementsToRegion_Time(self):
        s = time()
        self.gb = GameBoardMethodsTest.sample_gameboard1()
        ##self.gb.assign_elements_to_region()
        rt = time() - s
        print("config:\n{}\n".format(self.gb.config))
        print("areaDiff :\n{}\n".format(self.gb.configAreaDiff))
        print("time :\t{}".format(rt))
        self.assertTrue(rt < 60, msg = "too slow")


"""
if __name__ == "__main__":
    unittest.main()
"""

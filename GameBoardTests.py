from GameBoard import *
import unittest
from time import time
from random import randrange

class GameBoardMethodsTest(unittest.TestCase):

    """
    description:
    - languages are of uniform size
    """
    @staticmethod
    def sample_gameboard1(assignElementsToRegion):
        # get languages with random centroids of uniform size
        languageInfo = []
        dim = (8,8)
        for i in range(5):
            languageInfo.append(Language.random(idn = i, mode = "const"))
        q = GameBoard(languageInfo, dim, assignElementsToRegion = assignElementsToRegion)
        return q

    """
    description:
    - sample gameboard with specification
    """
    @staticmethod
    def sample_gameboard2():
        # specs.
        sizesInfo = [(400, 10), (2000, 30), (1000, 20)]
        languageInfo = []
        dim = (8,8)

        for i, s in enumerate(sizesInfo):
            languageInfo.append(Language.random(idn = i,\
                minSizeInfo = s[0], startSizeInfo = s[1], mode = "const"))
        return GameBoard(languageInfo, dim)

    """
    description:
    - sample gameboard with random languages of equal size
    """
    @staticmethod
    def sample_gameboard3(numLanguages, assignElementsToRegion):
        randomSizes = [randrange(20, 300)]
        languageInfo = []
        dim = (8,8)
        for i in range(numLanguages):
            languageInfo.append(Language.random(idn = i,\
                minSizeInfo = randomSizes, startSizeInfo = 4, mode = "geq"))
        return GameBoard(languageInfo, dim, assignElementsToRegion = assignElementsToRegion)

    def setUp(self):
        self.gb = None

    """
    description:
    - checks if assignment takes place for `assignElementsToRegion` set to False.
    """
    def test_GameBoard_AssignElementsToRegion_SetToFalse(self):
        s = time()
        self.gb = GameBoardMethodsTest.sample_gameboard1(False)
        rt = time() - s
        print("test 1 config:\n{}\n".format(self.gb.config))
        print("test 1 areaDiff :\n{}\n".format(self.gb.configAreaDiff))
        print("test 1 time :\t{}".format(rt))

    def test_GameBoard_AssignElementsToRegion_TrialAndError_RandomSizedLanguages(self):
        s = time()
        numLanguages = 5
        assignElementsToRegion = ("t/e", 1)
        gb = GameBoardMethodsTest.sample_gameboard3(numLanguages = numLanguages,\
            assignElementsToRegion = assignElementsToRegion)
        rt = time() - s
        print("test 2 config:\n{}\n".format(gb.config))
        print("test 2 areaDiff :\n{}\n".format(gb.configAreaDiff))
        print("test 2 time :\t{}".format(rt))

    def test_GameBoard_AssignElementsToRegion_BestFit_RandomSizedLanguages(self):
        s = time()
        numLanguages = 5
        assignElementsToRegion = ("fit", 1)
        gb = GameBoardMethodsTest.sample_gameboard3(numLanguages = numLanguages,\
            assignElementsToRegion = assignElementsToRegion)
        rt = time() - s
        print("test 3 config:\n{}\n".format(gb.config))
        print("test 3 areaDiff :\n{}\n".format(gb.configAreaDiff))
        print("test 3 time :\t{}".format(rt))

if __name__ == "__main__":
    unittest.main()

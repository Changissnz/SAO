from GameBoard import *
import unittest

class GameBoardMethodsTest(unittest.TestCase):

    def setUp(self):

        # get languages with random centroids
        languageInfo = []
        dim = (8,8)
        for i in range(5):
            languageInfo.append(Language.random(idn = i, mode = "const"))
        self.gb = GameBoard(languageInfo, dim)

        # print out element info
        print("gb language count :\t", self.gb.elementLanguageCount)
        return -1

    # TODO : test areaDiff
    def test_GameBoard_AssignElementsToRegion(self):
        ##self.setUp()
        self.gb.assign_elements_to_region()
        print("config:\n{}\n".format(self.config))
        print("areaDiff :\n{}\n".format(self.configAreaDiff))


if __name__ == "__main__":
    unittest.main()

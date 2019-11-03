from ShameAndObedienceGameBoard import *
from ShameAndObedienceElementTests import *
import unittest

# TODO : test pixel res

class ShameAndObedienceGameBoardMethodsTest(unittest.TestCase):

    @staticmethod
    def sample_action_functions():
        shameFunc = make_func_float_by_threshold_standard(0.0, 1.0)
        alignFunc = make_func_float_by_threshold_standard(0.0, 1.0)
        funcInfo = {"shame" : shameFunc, "align" : alignFunc}
        return funcInfo

    @staticmethod
    def sample_action_functions_multiplier():
        shameFunc = multiplier_function(minVal = 0.25, maxVal = 0.5, k = 1)
        alignFunc = multiplier_function(minVal = 0.5, maxVal = 0.75, k = 1)
        funcInfo = {"shame" : shameFunc, "align" : alignFunc}
        return funcInfo

    @staticmethod
    def sample_action_functions_exponential():
        shameFunc = exponential_function_restricted(minVal = 0.15, maxVal = 0.3, k = 2)
        alignFunc = exponential_function_restricted(minVal = 0.10, maxVal = 0.35, k = 2)
        funcInfo = {"shame" : shameFunc, "align" : alignFunc}
        return funcInfo

    # TODO : refactor duplicate
    @staticmethod
    def sample_gameboard1(assignElementsToRegion = False):
        # get languages with random centroids of uniform size
        languageInfo = []
        dim = (8,8)
        for i in range(5):
            languageInfo.append(Language.random(idn = i, mode = "const"))
        q = ShameAndObedienceGameBoard(languageInfo, dim, pixelRes = (1000,750),\
            assignElementsToRegion = assignElementsToRegion)

        ## set action functions
        #q.set_action_functions(ShameAndObedienceGameBoardMethodsTest.sample_action_functions())
        q.set_action_functions(ShameAndObedienceGameBoardMethodsTest.sample_action_functions_multiplier())
        return q

    @staticmethod
    def sample_gameboard2():
        sampleLanguages = ShameAndObedienceElementMethodsTest.test_sample_languages_1()
        gb = ShameAndObedienceGameBoard(sampleLanguages, (8,8), pixelRes = (1000, 750),\
            assignElementsToRegion = 200)
        gb.set_action_functions(ShameAndObedienceGameBoardMethodsTest.sample_action_functions_multiplier())
        return gb
    """
    description:
    - makes a gameboard with random elements with declared
      overlapping centroids
    """
    @staticmethod
    def sample_gameboard_random_elements_and_premate():
        return -1

    """
    description:
    -
    """
    def setUp(self):

        # set up the first gameboard
        # consists of random languages
        self.gb = ShameAndObedienceGameBoardMethodsTest.sample_gameboard1()

        # get sample languages
        sampleLanguages = ShameAndObedienceElementMethodsTest.test_sample_languages_1()
        self.gb2 = ShameAndObedienceGameBoard(sampleLanguages, (8,8), pixelRes = (1000,750), assignElementsToRegion = False)
        self.gb2.set_action_functions(ShameAndObedienceGameBoardMethodsTest.sample_action_functions_multiplier())

    def test_ShameAndObedienceGameBoard_PaintGameBoard(self):
        ##self.gb.paint_elements()
        #print("AREADIFF :\t", self.gb.configAreaDiff)
        return

    def test_ShameAndObedienceElement_analysis_gameboard2(self):
        e1, e2 = self.gb2.elements[3], self.gb2.elements[4]
        ov1, ov2 = ShameAndObedienceElement.get_element_language_overlap_measures(e1, e2)
        d1, d2 = ShameAndObedienceElement.get_element_language_disjoint_measures(e1, e2)
        print("overlap measures : {} / {}".format(ov1, ov2))
        print("disjoint measures : {} / {}".format(d1, d2))

    def test_demonstrate_ShameAndObedienceGameBoard_run(self):
        ## uncomment below run
        '''
        numRuns = 5
        self.gb2.run(numRounds = numRuns)
        '''
        return

    def test_demonstrate_ShameAndObedienceGameBoard_run_and_visualize(self):
        gb3 = ShameAndObedienceGameBoardMethodsTest.sample_gameboard2()

        # order might be mixed up
        for k in gb3.elements.values():
            print("element location :\t", k.location)
        return

if __name__ == "__main__":
    unittest.main()

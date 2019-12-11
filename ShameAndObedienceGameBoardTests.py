from ShameAndObedienceGameBoardTestVariables import *
import unittest
from time import time

class ShameAndObedienceGameBoardMethodsTest(unittest.TestCase):

    """
    description:
    - makes a gameboard with random elements with declared
      overlapping centroids
    """
    @staticmethod
    def sample_gameboard_random_elements_and_premate():
        return -1

    def test_ShameAndObedienceElement_analysis_gameboard2(self):
        sampleLanguages = ShameAndObedienceGameBoardTestVariables.test_sample_languages_1()

        gb = ShameAndObedienceGameBoard(sampleLanguages, (8,8),\
            pixelRes = (1000,750), assignElementsToRegion = False,\
            actionFunctions = ShameAndObedienceGameBoardTestVariables.sample_action_functions_multiplier())
        e1, e2 = gb.elements[3], gb.elements[4]
        ov1, ov2 = ShameAndObedienceElement.get_element_language_overlap_measures(e1, e2)
        d1, d2 = ShameAndObedienceElement.get_element_language_disjoint_measures(e1, e2)
        
        #0.8571428571428571 / 0.8571428571428571
        #disjoint measures : 0.0 / 0.0
        self.assertAlmostEqual(0.86, ov1, 2)
        self.assertAlmostEqual(0.86, ov2, 2)
        self.assertAlmostEqual(0, d1, 2)
        self.assertAlmostEqual(0, d2, 2)
                
    ###################### INITIALIZATION METHODS FOR GAMEBOARD OF DIFFERENT ASSIGNMENTS

    ## uncomment below to run initialization by fit
    """
    def test_demonstrate_ShameAndObedienceGameBoard_run_with_assign_for_fit(self):
        t = time()
        assignElementsToRegion = ("fit", 4)
        gb = ShameAndObedienceGameBoardTestVariables.sample_gameboard2(assignElementsToRegion)
        rt = time() - t

        print("total runtime for assign fit:\t", rt)
        print("area difference :\t", gb.configAreaDiff)
        print("-----------------------------------------")
    """ 

    ## uncomment below to run initialization by t/e
    """
    def test_demonstrate_ShameAndObedienceGameBoard_run_with_assign_for_random(self):
        t = time()
        assignElementsToRegion = ("t/e", 4)
        gb = ShameAndObedienceGameBoardTestVariables.sample_gameboard2(assignElementsToRegion)
        rt = time() - t

        print("total runtime for assign t/e:\t", rt)
        print("area difference :\t", gb.configAreaDiff)
        print("-----------------------------------------")
    """
    
    # TODO : DELETE THIS !! 
    ## uncomment below for vis.
    """
    def test_demonstrate_ShameAndObedienceGameBoard_run_n_rounds_no_visualization(self, n = 15):

        assignElementsToRegion = ("t/e", 2)
        gb = ShameAndObedienceGameBoardTestVariables.sample_gameboard2(assignElementsToRegion)
        t = time()
        n_ = n
        while n_ > 0 and not gb.finish:
            gb.move_one()
            print("moving one")
            n_ -= 1
        print("runtime : {}\trounds run : {}\t".format(time() - t, n - n_))
    """


if __name__ == "__main__":
    unittest.main()

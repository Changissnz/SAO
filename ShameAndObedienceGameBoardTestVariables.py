"""
this file will contain test variables for ShameAndObedienceGameBoard
"""

from ShameAndObedienceGameBoard import *
from ShameAndObedienceElementTests import *
# TODO : test pixel res

class ShameAndObedienceGameBoardTestVariables():

    ####################### ACTION FUNCTIONS USED FOR TESTING
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

    ####################### GAMEBOARDS FUNCTIONS USED FOR TESTING

    """
    description:
    - gameboard of arbitrary languages of same size
    """
    @staticmethod
    def sample_gameboard1(assignElementsToRegion = False):
        # get languages with random centroids of uniform size
        languageInfo = []
        dim = (8,8)
        for i in range(5):
            languageInfo.append(Language.random(idn = i, mode = "const"))
        q = ShameAndObedienceGameBoard(languageInfo, dim, pixelRes = (1000,750),\
            assignElementsToRegion = assignElementsToRegion, actionFunctions = ShameAndObedienceGameBoardMethodsTest.sample_action_functions_multiplier())
        return q

    """
    description:
    - gameboard that uses languages of sample 1
    """
    @staticmethod
    def sample_gameboard2(assignElementsToRegion):
        sampleLanguages = ShameAndObedienceGameBoardTestVariables.test_sample_languages_1()
        saf = ShameAndObedienceGameBoardTestVariables.sample_action_functions_multiplier()

        gb = ShameAndObedienceGameBoard(sampleLanguages, (8,8), pixelRes = (1000, 750),\
            assignElementsToRegion = assignElementsToRegion, actionFunctions = saf)
        return gb

    @staticmethod
    def sample_gameboard3(assignElementsToRegion):
        sampleLanguages = ShameAndObedienceGameBoardTestVariables.test_sample_languages_1()

        return -1

    @staticmethod
    def test_sample_languages_1():

        c1 = {"dog", "whistle"}
        c2 = {"cat", "whistle"}
        c3 = {"dog", "cat", "mountain"}
        c4 = {"weird"}
        c5 = {"weird", "weird"}
        centroidsForEach = [c1,c2,c3,c4, c5]
        languages = []

        for (i, c) in enumerate(centroidsForEach):

            l = Language.random_by_centroid(idn = i, centroids = c, languageOutput = list,\
                        minSizeInfo = 100, startSizeInfo = 5, mode = "geq")
            #print("LANGUAGE :\t", l)
            #print("\ncontents :\t", l.language)
            languages.append(l)
        return languages

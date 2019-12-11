from GameBoardHandler import *
import unittest
from time import time

## TODO : methods that need to be tested.
"""
assign_elements_to_regions_using_info_by_swiss_cheese(elementInfo, gameboardDim, numConfigAttempts = 5)
assign_helper(elementInfo, gameboardDim, numRandomPoints = 1000)

"""


class GameBoardHandlerMethodsTests(unittest.TestCase):

    def test_GameBoardHandler_GetDistanceBetweenCoordinates(self):
        c1 = (0, 0)
        c2 = (2, 2)
        d = abs(GameBoardHandler.get_distance_between_coordinates(c1,c2) - sqrt(8))
        self.assertTrue(d <= 0.001)

    def test_GameBoardHandler_ChooseRandomPointInRadius(self):
        radius = 2
        point = (4, 2)
        for i in range(100):
            p = GameBoardHandler.choose_random_point_in_radius(point, radius)
            self.assertTrue(abs(p[0] - point[0]) <= radius, "[0] random : {}\point : {}".format(abs(p[0] - point[0]), radius))
            self.assertTrue(abs(p[1] - point[1]) <= radius)

    def test_GameBoardHandler_ChooseNPoints(self):

        numPoints = 1000 # this will not work : 10000
        coordinateRange = (300, 300)
        setOfCoordinates = {(5, 100), (10, 101), (20, 35)}
        minDistance = 5
        x = GameBoardHandler.choose_n_points(numPoints, coordinateRange, setOfCoordinates, minDistance)
        self.assertTrue(len(x) == numPoints)

    def test_GameBoardHandler_GetFactorsFor(self):
        x = 1000
        q = GameBoardHandler.get_factors_for(x, 5)
        self.assertTrue(len(q) == 5, "want {} elements, got {}".format(5, len(q)))
        for q_ in q:
            self.assertTrue(q_[0] * q_[1] == 1000, "want 1000 got {}".format(q_[0] * q_[1]))

    def test_GameBoardHandler_GetBestConfigRegionUsingInspectionPoints_Accuracy(self):

        gameboardDim = (8, 8)
        wantedDim = (2,2)

        # case 1
        currentConfig = []
        q = GameBoardHandler.get_best_config_region_using_inspection_points(\
            gameboardDim, wantedDim, currentConfig, numRandomPoints = 10, calibrateMode = "square", cutOff = "auto")

        self.assertTrue(q[1] < 0.05, "configuration not accurate")

        # case 2
        currentConfig = [((0,0), (2,2))]
        q = GameBoardHandler.get_best_config_region_using_inspection_points(\
            gameboardDim, wantedDim, currentConfig, numRandomPoints = 10, calibrateMode = "square", cutOff = "auto")

        self.assertTrue(q[1] < 0.05, "configuration not accurate")

    def test_GameBoardHandler_GetBestConfigRegionUsingInspectionPoints_Accuracy(self):
        gameboardDim = (8, 8)
        wantedDim = (2,2)

        # case 1
        currentConfig = []
        s = time()
        q = GameBoardHandler.get_best_config_region_using_inspection_points(\
            gameboardDim, wantedDim, currentConfig, numRandomPoints = 10, calibrateMode = "square", cutOff = None)
        rt = time() - s
        print("Q:\t", q[0])
        print("Q2:\t", q[1])
        print("time 1 :\t", rt)
        self.assertTrue(rt < 20, "[1] could not get best config not fast enough : {}".format(rt))

        currentConfig.append(q[0])
        s = time()
        q = GameBoardHandler.get_best_config_region_using_inspection_points(\
            gameboardDim, wantedDim, currentConfig, numRandomPoints = 10, calibrateMode = "square", cutOff = None)
        rt = time() - s
        print("[1] Q:\t", q[0])
        print("[1] Q2:\t", q[1])
        print("time 1 :\t", rt)

        # case 2
        currentConfig = [((0,0), (2,2))]
        s = time()
        q = GameBoardHandler.get_best_config_region_using_inspection_points(\
            gameboardDim, wantedDim, currentConfig, numRandomPoints = 10, calibrateMode = "square", cutOff = None)
        rt = time() - s
        print("time 2 :\t", rt)
        print("q :\t", q)
        self.assertTrue(rt < 20, "[2] could not get best config not fast enough : {}".format(rt))

if __name__ == '__main__':
    unittest.main()

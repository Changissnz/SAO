from GameBoardHandler import *
import unittest

class GameBoardHandlerMethodsTests(unittest.TestCase):

    '''
    '''
    def test_GameBoardHandler_GetDistanceBetweenCoordinates(self):
        c1 = (0, 0)
        c2 = (2, 2)
        d = abs(GameBoardHandler.get_distance_between_coordinates(c1,c2) - sqrt(8))
        self.assertTrue(d <= 0.001)

    '''
    '''
    def test_GameBoardHandler_ChooseRandomPointInRadius(self):
        radius = 2
        point = (4, 2)
        for i in range(100):
            p = GameBoardHandler.choose_random_point_in_radius(point, radius)
            self.assertTrue(abs(p[0] - point[0]) <= radius, "[0] random : {}\point : {}".format(abs(p[0] - point[0]), radius))
            self.assertTrue(abs(p[1] - point[1]) <= radius)

    '''
    '''
    # TODO make assertion
    def test_GameBoardHandler_ChooseNPoints(self):

        numPoints = 1000 # this will not work : 10000
        coordinateRange = (300, 300)
        setOfCoordinates = {(5, 100), (10, 101), (20, 35)}
        minDistance = 5
        x = GameBoardHandler.choose_n_points(numPoints, coordinateRange, setOfCoordinates, minDistance)
        assert len(x) == numPoints

    @staticmethod
    def test_GameBoardHandler_ChooseNPoints():
#     def choose_unused_random_points_in_radius(p, radius, numPoints, setOfCoordinates, minDistance):

        return -1

    '''
    '''
    def test_GameBoardHandler_GetFactorsFor(self):
        x = 1000
        q = GameBoardHandler.get_factors_for(x, 5)
        self.assertTrue(len(q) == 5, "want {} elements, got {}".format(5, len(q)))
        for q_ in q:
            self.assertTrue(q_[0] * q_[1] == 1000, "want 1000 got {}".format(q_[0] * q_[1]))

if __name__ == '__main__':
    unittest.main()

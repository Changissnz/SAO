'''
this is a class that handles coordinate calculations for its
GameBoard
'''
from math import sqrt
from random import uniform, random, shuffle
from copy import deepcopy

class GameBoardHandler:

    def __init__(self):
        return

    '''
    description:
    - calculates the squared difference between two coordinates

    arguments:
    - coord1 := tuple(int)::(1-dim)
    - coord2 := tuple(int)::(2-dim)

    return:
    - float >= 0
    '''
    @staticmethod
    def get_distance_between_coordinates(coord1, coord2):
        assert len(coord1) == 2 and len(coord2) == len(coord1), "only 2-dimensions are permitted."
        return sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2 )

    '''
    description:
    - determines if point x is at least minimum distance from all other coordinates

    arguments:
    - c := (int::(x), int::(y))
    - otherCoordinates := set((int::(x), int::(y)))
    - minDistance := float

    return:
    - bool
    '''
    @staticmethod
    def is_coordinate_far_enough(c, otherCoordinates, minDistance):
        for x in otherCoordinates:
            if GameBoardHandler.get_distance_between_coordinates(c, x) <= minDistance:
                return False
        return True

    '''
    description:
    - chooses n centroids on game board

    arguments:
    - numCentroids := int
    - coordinateRange := (int::(maxX), int::(maxY))
    - setOfCoordinates := list((int::(x), int::(y)))
    - minDistance := "auto"|float

    return:
    - list((int::(x), int::(y)))
    '''
    @staticmethod
    def choose_n_points(numCentroids, coordinateRange, setOfCoordinates, minDistance = "auto"):

        if minDistance == "auto":
            minDistance = (coordinateRange[0] * coordinateRange[1]) / (2 * numCentroids)

        otherCoordinates = deepcopy(setOfCoordinates)
        centroids = []
        while len(centroids) < numCentroids:
            x = (uniform(0, coordinateRange[0]), uniform(0, coordinateRange[1]))
            if GameBoardHandler.is_coordinate_far_enough(x, otherCoordinates, minDistance):
                otherCoordinates.add(x)
                centroids.append(x)
        return centroids

    '''
    description:
    - chooses a random coordinate in the ball radius of some point p

    arguments:
    - p := (int::(x), int::(y))
    - radius := float >= 0

    return:
    - (int::(x), int::(y))
    '''
    @staticmethod
    def choose_random_point_in_radius(p, radius):
        p_ = []
        for p1 in p:
            px = uniform(0, radius)
            px = -px if random() < 0.5 else px
            p_.append(p1 + px)
        return tuple(p_)

    @staticmethod
    def choose_random_points_in_radius(p, radius, numPoints):
        p_ = []
        for i in range(numPoints):
            p1 = GameBoardHandler.choose_random_point_in_radius(p, radius)
            p_.append(p1)
        return p_

    '''
    description:
    - chooses n random points that take into account existing points

    arguments:
    - p := (float, float), reference point
    - r := float, radius
    - numPoints := int, required number of points to get
    - setOfCoordinates := set((float,float)), existing coordinates to be aware of
    - minDistance := float

    return:
    - set((float,float))
    '''
    @staticmethod
    def choose_unused_random_points_in_radius(p, radius, numPoints, setOfCoordinates, minDistance):
        newPoints = {}

        otherCoordinates = deepcopy(setOfCoordinates)
        while numPoints > 0:
            points = GameBoardHandler.choose_random_points_in_radius(p, radius, numPoints)

            for p in points:
                if GameBoardHandler.is_coordinate_far_enough(p, otherCoordinates, minDistance):
                    newPoints.add(p)
                    numPoints -= 1
        return newPoints

    """
    description:
    -

    arguments:
    - gameboard := GameBoard
    - mode := size-net|influence

    return:
    - list((x, y)), x and y are length and width values for each element
    OR
    - False (check error)
    """
    # TODO : test this
    @staticmethod
    def calculate_proportions_for_elements(gameboard, mode = "size-net"):

        assert mode in {"size-net", "influence"}, "mode {} is invalid".format(mode)
        areas = []
        if mode == "size-net":
            totalSize = 0
            for i, e in enumerate(gameboard.elements):
                sz = len(gameboard.elements[i].language.language[1])
                areas.append(sz)
                totalSize += sz
            try:
                return [a / totalSize for a in areas]
            except:
                return False # no language contents
        else:
            raise ValueError("mode {} has not yet been implemented".format(mode))

    """

    arguments:
    - mode := size-net|influence
    """
    @staticmethod
    def calculate_areas_for_elements(gameboard, mode = "size-net"):

        """
        description:
        - rounding algorithm

        arguments:
        - ea := list(float)

        return:
        - list
        """
        def rounding_alg(ea):
            return [int(round(e,0)) for e in ea]

        totalArea = gameboard.get_area()
        proportions = GameBoardHandler.calculate_proportions_for_elements(gameboard, mode)
        assert proportions != False, "could not compute"

        # areas in floats, need to round up or down one
        elementAreas = [p * totalArea for p in proportions]
        elementAreas = rounding_alg(elementAreas)
        elementAreas = [GameBoardHandler.get_random_factor_pair(e) for e in elementAreas]
        return elementAreas


    """
    description:
    -

    arguments:
    - criteria := "net"|"set"


    """
    @staticmethod
    def calculate_radius_by_criteria(criteria = "sadfsdaf"):
        return -1

    '''
    description:
    - gets q number of factors for some integer, in which if there are more than
      `numFactors` factor pairs, `numFactors` number of factors will be returned,

    arguments:
    - i := int
    - numFactors := int, number of factors to get

    return:
    - list((int,int))
    '''
    # TODO : test this, make for-loop efficient
    @staticmethod
    def get_factors_for(i, numFactors):
        factorPairs = set()
        for j in range(1, i + 1):
            if numFactors == 0:
                break
            q = i // j
            if j * q == i:
                factorPairs.add((j, q) if j < q else (q, j))
                numFactors -= 1
        return factorPairs

    '''
    description:
    - gets a random factor pair for integer

    arguments:
    - i := int

    return:
    - (int,int)
    '''
    # TODO : make this func better
    @staticmethod
    def get_random_factor_pair(i):
        q = GameBoardHandler.get_factors_for(i, 5)
        shuffle(q)
        return q[0]

    '''
    description:
    - gets the factor pair for integer with the least pairwise distance.

    arguments:
    - i := int

    return:
    - (int,int)
    '''
    @staticmethod
    def get_closest_factor_pair(i):
        return -1

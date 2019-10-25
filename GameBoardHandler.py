'''
this is a class that handles coordinate calculations for its
GameBoard
'''
from math import sqrt
from random import uniform, random, shuffle
from copy import deepcopy
from FreeAndSimpleScanner import *

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
            minDistance = (coordinateRange[0] * coordinateRange[1]) / (2000)

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
    - an unused point must be at least `minDistance` from all other points

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
                    otherCoordinates.add(p)
                    numPoints -= 1
        return newPoints

    # TODO : test this
    '''
    description:
    - make sure targetRegion has area > some threshold

    arguments:
    - numPoints := int
    - targetRegion := ((int,int), (int,int)), a proper region
    - usedRegions := list((int,int),(int,int)), list of proper regions

    return:
    - set((int::x,int::y))
    '''
    @staticmethod
    def choose_unused_random_points_by_region(numPoints, targetRegion, usedRegions, minThresholdArea = 0):

        if not GameBoardHandler.is_region_free_by_area(targetRegion, usedRegions, minThresholdArea):
            return False

        q = set()
        while len(q) < numPoints:
            x, y = uniform(targetRegion[0][0], targetRegion[1][0]),\
                uniform(targetRegion[0][1], targetRegion[1][1])

            if FreeAndSimpleScanner.is_coordinate_free((x,y), usedRegions):
                q.add((x,y))
        return q

    # TODO : test this
    @staticmethod
    def is_region_free_by_area(targetRegion, usedRegions, minThresholdArea = 0):
        a = AreaScanner.sloppy_area_scan(targetRegion, usedRegions, increment = 10**(-2))
        if a == False:
            return False
        return True if a > minThresholdArea else False

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

    #-----------------------------------------

    ########### START : code for assigning elements to regions here

    @staticmethod
    def is_valid_point_to_area_ratio(numPoints, area, req = 1.5):
        #requirement : p/a < 1.5
        try:
            return True if numPoints/ area < req else False
        except: return False

    """
    description:
    - this is an algorithm designed to scan for the greatest area by the
      'swiss-cheese' method below:
      - the 'swiss-cheese' method uses randomized blotting of the region
      - each blot will be located on an unused region and do,
      -     attempt to fetch a region
      -     compare with and update best region
      - there will be a maximum of n blots
      - if n is set to auto, will use the formula:
      -     area(gameboard) * 2000

    arguments:
    - gameboardDim := (int,int)
    - usedRegions := list(((int::(minX), int::(minY)), (int::(maxX), int::(maxY))))
    - n := int|auto

    return:
    - ((int::(minX), int::(minY)), (int::(maxX), int::(maxY)))|False
    """
    @staticmethod
    def scan_by_swiss_cheese_for_max(gameboardDim, usedRegions, n = "auto"):
        if n == "auto":
            n = FreeAndSimpleScanner.get_area_of_region(((0,0),gameboardDim)) * 2000

        # get n unused points
        points = GameBoardHandler.choose_unused_random_points_by_region(n, ((0,0), gameboardDim), usedRegions)
        if points == False: return False

        maxRegion = None
        maxArea = None

        for p in points:
            q = AreaScanner.get_best_region_given_coordinates(p, gameboardDim, usedRegions, increment = 10**(-2))
            if q is False: continue
            r,a = q

            if maxRegion == None:
                maxRegion,maxArea = r,a
            elif maxArea < a:
                maxRegion,maxArea = r,a

        return maxRegion, maxArea

    ####### START : the assignment algorithm for elements in Shame And Obedience

    """
    description:
    -

    arguments:
    - elementInfo := list, of (key,values),
                    keys are int::(elementId), values are int::(wantedSquareDim)
    - gameboardDim := (int,int)

    """
    @staticmethod
    def assign_elements_to_regions_using_info_by_swiss_cheese(elementInfo, gameboardDim, numConfigAttempts = 5):
        if len(elementInfo) == 0: return False

        if not GameBoardHandler.is_valid_point_to_area_ratio(len(elementInfo), gameboardDim[0] * gameboardDim[1]):
            return False

        # keep track of the lowest area difference
        bestConfig = None
        lowestAreaDifference = None

        for i in range(numConfigAttempts):
            config, ad = GameBoardHandler.assign_helper(elementInfo, gameboardDim, numRandomPoints = 1000) # last arg.?
            if GameBoardHandler.is_valid_config(config):

                if bestConfig == None:
                    bestConfig, lowestAreaDifference = config, ad
                elif lowestAreaDifference > ad:
                    bestConfig, lowestAreaDifference = config, ad
        return bestConfig, lowestAreaDifference

    '''
    description:
    - method helps with assigning the best region for each element in element
    - method goes as follows:
    -

    arguments:
    - elementInfo := list, of (key,values),
                    keys are int::(elementId), values are int::(wantedSquareDim)
    - gameboardDim := (int,int)

    return:
    - list, of (key,values),
        keys are int::(elementId), values are (`regions`, `freeArea`)
    '''
    @staticmethod
    def assign_helper(elementInfo, gameboardDim, numRandomPoints = 1000):

        def helper_func(rp):
            bestRegion = None
            bestRegionAreaDiff = None
            for p in rp:
                r = AreaScanner.get_best_region_fit_given_wanted_dimensions(p, gameboardDim, (e[1],e[1]), currentConfig, increment = 10**(-2))
                if r == False:
                    continue
                elif bestRegion == None:
                    bestRegion = r[0]
                    bestRegionAreaDiff = abs(r[1] - e[1]**2)
                else:
                    q = abs(r[1] - e[1]**2)
                    if bestRegionAreaDiff > q:
                        bestRegion, bestRegionAreaDiff = r[0], q
            return bestRegion, bestRegionAreaDiff

        shuffle(elementInfo)

        # these are the default check points
        defaultPoints = [(0,0), (0,gameboardDim[1]), (gameboardDim[0], 0), gameboardDim]

        # iterate through elementInfo
        currentConfig = []
        configAreaDiff = 0

        for e in elementInfo:
            # get random points for elements
            points = GameBoardHandler.choose_unused_random_points_by_region(numRandomPoints,\
                ((0,0), gameboardDim), currentConfig, 0)
            rndmPts = defaultPoints + list(points)

            br, brad = helper_func(rndmPts)
            currentConfig.append(br)
            if br != None:
                configAreaDiff += brad
        return currentConfig, configAreaDiff

    @staticmethod
    def is_valid_config(config):
        for c in config:
            if c == None: return False
        return True


    @staticmethod
    def get_config_tmp_func(elementInfo, gameboardDim, numRandomPoints = 10):

        def helper_func(rp):
            bestRegion = None
            bestRegionAreaDiff = None
            for p in rp:
                r = AreaScanner.get_best_region_fit_given_wanted_dimensions(p, gameboardDim, (e[1],e[1]), currentConfig, increment = 10**(0))
                if r == False:
                    continue
                elif bestRegion == None:
                    bestRegion = r[0]
                    bestRegionAreaDiff = abs(r[1] - e[1]**2)
                else:
                    q = abs(r[1] - e[1]**2)
                    if bestRegionAreaDiff > q:
                        bestRegion, bestRegionAreaDiff = r[0], q
            return bestRegion, bestRegionAreaDiff

        defaultPoints = [(0,0), (0,gameboardDim[1]), (gameboardDim[0], 0), gameboardDim]
        currentConfig = []
        configAreaDiff = 0

        for e in elementInfo:
            # get random points for elements
            points = GameBoardHandler.choose_unused_random_points_by_region(numRandomPoints,\
                ((0,0), gameboardDim), currentConfig, 0)
            rndmPts = defaultPoints + list(points)

            br, brad = helper_func(rndmPts)
            currentConfig.append(br)
            if br != None:
                configAreaDiff += brad

        return currentConfig, configAreaDiff



    ####### END : the assignment algorithm for elements in Shame And Obedience
    ########### END : code for assigning elements to regions here

'''
this is a class that handles coordinate calculations for its
GameBoard
'''
from math import sqrt
from random import uniform, random, shuffle
from copy import deepcopy
from FreeAndSimpleScanner import *
from multiprocessing import Pool

## TODO : bug in square calibration


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

    ################ START : methods below are currently not used

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

    ################ END : methods below are currently not used

    ########### START : code for assigning elements to regions here

    @staticmethod
    def is_valid_point_to_area_ratio(numPoints, area, req = 1.5):
        #requirement : p/a < 1.5
        try:
            return True if numPoints/ area < req else False
        except: return False

    ####### START : the assignment algorithm for elements in Shame And Obedience

    """
    description:
    - determines if configuration is valid or not.

    arguments:
    - config := list(`region`)

    return:
    - bool

    @staticmethod
    def is_valid_config(config):
        for c in config:
            if c == None: return False
        return True
    """

    """
    description:
    - this is a wrapper function to select the best region of fit at coordinate p

    arguments:
    - p := ~
    - gameboardDim := ~
    - wantedDim := ~
    - usedRegions := ~
    - calibrateMode := ~

    return:
    - `region`, `free area`
    """
    @staticmethod
    def x(p, gameboardDim, wantedDim, usedRegions, calibrateMode = "square"):
        q = AreaScanner.get_best_region_fit_given_wanted_dimensions(p, gameboardDim,\
            wantedDim, usedRegions, increment = 10**(-2), calibrateMode = calibrateMode)
        ##print("HERE2:\t", q)
        return q

    ## TODO : there is a bug in `calibrate_region_into_square`
    @staticmethod
    def y(wantedDim, gameboardDim, usedRegions, calibrateMode, p):
        q = AreaScanner.get_best_region_fit_given_wanted_dimensions(p, gameboardDim,\
            wantedDim, usedRegions, increment = 10**(-2), calibrateMode = calibrateMode)
        ##print("HERE2:\t", q)
        if q == False:
            return q
        if q[1] == False:
            return q[1]

        ##print("IS SQUARE REGION :\t", FreeAndSimpleScanner.is_square_region(q[0]))
        if calibrateMode == "square":
            if not FreeAndSimpleScanner.is_square_region(q[0]):
                ##print("NOT SQUARE")
                return False

        x = abs(q[1] - (wantedDim[0] * wantedDim[1]))
        return q[0], x



    """
    description:
    - gets the best region given `wantedDim` and `currentConfig`.
    - inspection points include gameboard corners.
    - number of point inspections can be set by `cutOff` mode

    arguments:
    ~

    return:
    - `region`, `area difference with wanted`
    """
    @staticmethod
    def get_best_config_region_using_inspection_points(gameboardDim, wantedDim, currentConfig, numRandomPoints = 10, calibrateMode = "square", cutOff = None):

        """
        description:
        - default points to check
        """
        def get_default_points():
            return [(0,0), (0,gameboardDim[1]), (gameboardDim[0], 0), gameboardDim]

        """
        description:
        - selecting points to check
        """
        def get_points_helper():
            pt = []
            defaultPoints = get_default_points()

            # check the default points
            for d in defaultPoints:
                if FreeAndSimpleScanner.is_coordinate_free(d, currentConfig):
                    #print("coord {} is free".format(d))
                    pt.append(d)

            # check below
            ##print("default points are :\t", pt)
            q = GameBoardHandler.choose_unused_random_points_by_region(numRandomPoints,\
                ((0,0), gameboardDim), currentConfig, 0)
            if q != False:
                return pt + list(q)
            return pt

        """
        description:
        - determines if region area diff satisfies cutOff
        """
        def cutoff():
            if cutOff is None:
                return False

            if bestAreaDiff < cutOff:
                return True
            return False

        # set cutOff
        if cutOff == "auto":
            cutOff = (gameboardDim[0] * gameboardDim[1]) / 500

        # get inspection points and set vars
        points = get_points_helper()
        bestRegion = None
        bestAreaDiff = None
        wantedArea = wantedDim[0] * wantedDim[1]

        ## regular approach without multiprocessing
        # iterate through points and get best region
        """
        for p in points:
            q = GameBoardHandler.x(p, gameboardDim, wantedDim, currentConfig, calibrateMode = "square")

            if q == False:
                continue

            if q[1] == False:
                continue

            # update best region
            if bestRegion == None:
                bestRegion, bestAreaDiff = q[0], abs(q[1] - wantedArea)
                if cutoff():
                    break

            else:
                x = abs(q[1] - wantedArea)
                if x < bestAreaDiff:
                    bestRegion, bestAreaDiff = q[0], x
                    if cutoff():
                        break
        """

        # multiprocessing alternative
        p = Pool(10)

        f = partial(GameBoardHandler.y, wantedDim, gameboardDim, currentConfig, calibrateMode)
        q = list(p.map(f, points))

        p.close()
        p.join()

        # filter values by false
        ##print("Q:\t", q)

        q = [r for r in q if r != False]
        if len(q) == 0:
            bestRegion, bestAreaDiff = None, None
        else:
            d = sorted(q, key = lambda kv: kv[1])[0]
            ##print("D here:\n{}\n\n".format(d))
            bestRegion, bestAreaDiff = d[0], d[1]
        return bestRegion, bestAreaDiff

    ##
    """
    description:
    - gets the best element-to-region configuration given `elementInfo`

    arguments:
    - element := list(int::(`elementId`), (int,int)::(`wanted dimensions`))
    - gameboardDim := (int,int)
    - numRandomPoints := int
    - calibrateMode := square|approximate
    - cutOff := None|auto|float::(0 <= x <= 1)

    return:
    - list((`elementId`, `wanted dimensions`, `best region`, `area difference with wanted`))
    - float::(net area difference)
    """
    @staticmethod
    def get_best_config_by_random_inspection(elementInfo, gameboardDim, numRandomPoints = 10, calibrateMode = "square", cutOff = None):
        # ? sort ?
        configInfo = []
        currentConfig = []
        currentAreaDiff = 0

        for k, v in elementInfo:

            q = 3
            while q > 0:

                br, bad = GameBoardHandler.get_best_config_region_using_inspection_points(\
                    gameboardDim, v, currentConfig, numRandomPoints = numRandomPoints,\
                    calibrateMode = calibrateMode, cutOff = cutOff)
                if br != None:
                    currentConfig.append(br)
                    configInfo.append((k, v, br, bad))
                    currentAreaDiff += bad
                    print("found region for {} : {}".format(k, br))
                    break
                q -= 1

        return configInfo, currentAreaDiff
    ####### END : the assignment algorithm for elements in Shame And Obedience
    ########### END : code for assigning elements to regions here

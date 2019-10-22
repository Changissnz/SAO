from copy import deepcopy

class FreeAndSimpleScanner:

    def __init__(self):
        return

    ########## START : methods on coordinates ################

    """
    description:
    - determines if coordinate is in region

    arguments:
    - coord := (int::(x), int::(y))
    - region := (int::(minX), int::(minY)), (int::(maxX), int::(maxY))

    return:
    - bool
    """
    @staticmethod
    def is_in_region(coord, region):
        # TODO make region check?
        assert FreeAndSimpleScanner.is_proper_region(region) is True, "invalid region {}".format(region)

        if not (coord[0] >= region[0][0] and coord[0] <= region[1][0]):
            return False
        if not (coord[1] >= region[0][1] and coord[0] <= region[1][1]):
            return False
        return True

    """
    description:
    - determines if coordinate is not in any region

    arguments:
    - coord := (int::(x), int::(y))

    return:
    - bool
    """
    @staticmethod
    def is_coordinate_free(coord, usedRegions):
        for r in usedRegions:
            if FreeAndSimpleScanner.is_in_region(coord, r):
                return False
        return True


    ########## END : methods on coordinates ################

    ########## START : methods on regions ################

    '''
    description:
    - makes a proper region out of a ((int,int), (int,int))

    arguments:
    - tuplePairOfPairs := ((int,int), (int,int))

    return:
    - region := ((int::(minX), int::(minY)), (int::(maxX), int::(maxY)))|False
    '''
    @staticmethod
    def to_proper_region(tuplePairOfPairs):
        assert len(tuplePairOfPairs) == 2, "invalid" # TODO make better check
        if tuplePairOfPairs[0][0] >= tuplePairOfPairs[1][0] or tuplePairOfPairs[0][1] >= tuplePairOfPairs[1][1]:
            tuplePairOfPairs = (tuplePairOfPairs[1], tuplePairOfPairs[0])
        if tuplePairOfPairs[0][0] >= tuplePairOfPairs[1][0] or tuplePairOfPairs[0][1] >= tuplePairOfPairs[1][1]:
            return False
        return tuplePairOfPairs

    '''
    description:
    ~

    arguments:
    - region := ((int::(minX), int::(minY)), (int::(maxX), int::(maxY))::(region))

    return:
    - float
    '''
    @staticmethod
    def get_area_of_region(region):
        if region == None: return 0
        if not FreeAndSimpleScanner.is_proper_region(region):
            return False
        m = abs(region[1][0] - region[0][0])
        n = abs(region[1][1] - region[0][1])
        return m * n

    """
    description:
    - returns the positive slope of a region ((0,0), dimensions)

    arguments:
    - dimensions := (int,int)

    return:
    - float
    """
    @staticmethod
    def get_slope_given_dimensions(dimensions):
        assert (dimensions[0] != 0 or dimensions[0] != 0), "dimensions cannot be zero, this is the real 2-d world"
        # get m
        return dimensions[1] / dimensions[0]

    """
    description:
    - determines if region is proper

    arguments:
    - region := ((int::(minX), int::(minY)), (int::(maxX), int::(maxY)))

    return:
    - float
    """
    @staticmethod
    def is_proper_region(region):
        try:
            assert type(region) is tuple and len(region) == 2, "invalid region {}".format(region)
            assert type(region[0]) is tuple and type(region[0]) is type(region[1]), "invalid region {}".format(region)
            assert len(region[0]) == 2 and type(region[0]) is type(region[1]), "invalid region {}".format(region)
            assert (region[1][0] - region[0][0]) >= 0 and (region[1][1] - region[0][1]) >= 0, "invalid region {}".format(region)
            return True
        except: return False

    """
    description:
    - calculates the upward (starts from left-top) or downward diagonal (starts from left-bottom)
      of a rectangular region

    arguments:
    - region := ((int::(minX), int::(minY)), (int::(maxX), int::(maxY))::(region))

    return:
    - int::(m), int::(b)
    """
    @staticmethod
    def get_diagonal_given_region(region, diagonal = "up"):
        assert diagonal in {'up', 'down'}, "invalid diagonal {}".format(diagonal)
        assert FreeAndSimpleScanner.is_proper_region(region) is True, "invalid region {}".format(region)

        if diagonal == "down":
            p1 = (region[0][0], region[1][1])
            p2 = (region[1][0], region[0][1])
        else:
            p1 = region[0]
            p2 = region[1]

        try:
            m = (p2[1] - p1[1]) / (p2[0] - p1[0])
            b = p1[1] - (m * p1[0]) # solve for b by p1
            return m, b
        except:
            return False

    ########## END : methods on regions ##################

    """
    description:
    - scans horizontally until free coordinate found

    arguments:
    - coord := (int,int)
    - gameboardDim := (int,int)
    - usedRegions := list(((int::(minX), int::(minY)), (int::(maxX), int::(maxY))))
    - direction := str, left|right|up|down
    - increment := float|auto

    return:
    - (int,int)|False
    """
    @staticmethod
    def line_scan_from_coordinate(coord, gameboardDim, usedRegions, direction = "left", increment = "auto"):
        assert direction in {'left', 'right', 'up', 'down'}, "direction {} invalid".format(direction)
        assert increment == "auto" or type(increment) is float, "invalid increment {}".format(increment)
        # calculate hop automatically by this schematic:
        if increment == "auto":
            increment = gameboardDim[0] / 1000
        else: assert increment >= 0, "invalid increment"

        if direction in {'left', 'down'}:
            increment = -1 * increment

        incrementos = lambda coord: (coord[0] + increment, coord[1]) if\
            direction in {'left', 'right'} else (coord[0], coord[1] + increment)
        clause = lambda c: True if c >= 0 and c <= gameboardDim[0] else False
        while clause(coord_):
            if FreeAndSimpleScanner.is_coordinate_free(coord_, usedRegions):
                return coord_
            coord_ = incrementos(coord_)
        return False

    # not thorough horizontal
    '''
    description:
    - performs a right angle scan starting from some coordinate

    arguments:
    - coord := (int,int)
    - gameboardDim := (int,int)
    - usedRegions := list(((int::(minX), int::(minY)), (int::(maxX), int::(maxY)))
    - angleDirectionX := str, left|right
    - angleDirectionY := str, up|down

    return:
    - ((int::(minX), int::(minY)), (int::(maxX), int::(maxY)))|False
    '''
    @staticmethod
    def right_angle_scan_from_coordinate(coord, gameboardDim, usedRegions, angleDirectionX, angleDirectionY):

        # get max/min values
        coordForX = FreeAndSimpleScanner.line_scan_from_coordinate(\
            coord, gameboardDim, usedRegions, direction = angleDirectionX, increment = "auto")

        coordForY =  FreeAndSimpleScanner.line_scan_from_coordinate(\
            coord, gameboardDim, usedRegions, direction = angleDirectionY, increment = "auto")

        region = (coord, (coordForX[0], coordForY[1]))
        region = FreeAndSimpleScanner.to_proper_region(region)
        return region

    ############# START : scanning algorithms

    '''
    description:
    - scan algorithm starts from upper-left on diagonal line of region.
    - iterates downward until other lower-right reached and do the following:
    -   scan left and right by right angles and look for the best region

    arguments:
    - coord := (int,int)
    - wantedArea := float
    - gameboardDim := (int,int)
    - usedRegions := list(((int::(minX), int::(minY)), (int::(maxX), int::(maxY)))

    return:
    -
    '''
    @staticmethod
    def scan_algorithm_1(coord, wantedArea, gameboardDim, usedRegions, increment = "auto"):
        # get diagonal
        # starting from upper left, travel down diagonal and run best scan

        # a small function that can cerTainly
        comparadantos = lambda r1, r2: r1 if\
            abs(wantedArea - FreeAndSimpleScanner.get_area_of_region(r1)) < \
            abs(wantedArea - FreeAndSimpleScanner.get_area_of_region(r2))\
            else r2

        def get_best_region(coordos, direction):
            assert direction in {'left', 'right'}, "direction {} invalid".format(direction)
            q = FreeAndSimpleScanner.line_scan_from_coordinate(coord, gameboardDim, usedRegions, direction, increment = "auto")
            if q is False:
                return False
            corordosWeuvas = coordos
            if direction == "left":
                # right-angle directions
                ## left, down
                f1 = ("left", "down")
                f2 = ("right", "up")
            else:
                f1 = ("left", "up")
                f2 = ("right", "down")
            e = FreeAndSimpleScanner.right_angle_scan_from_coordinate(corordosWeuvas, gameboardDim, usedRegions, f1[0], f1[1])
            e2 = FreeAndSimpleScanner.right_angle_scan_from_coordinate(corordosWeuvas, gameboardDim, usedRegions, f2[0], f2[1])
            return comparadantos(e,e2)

        def get_best_region_from_horizon(coordos, direction):
            assert direction in {'left', 'right'}, "direction {} invalid".format(direction)
            coordos_ = [coordos[0], coordos[1]]
            bestRegion = None

            while True:
                x = get_best_region(coordos_, direction)
                if x == False: break

                if bestRegion is None:
                    bestRegion = x
                else:
                    bestRegion = comparadantos(bestRegion,x)

                # update coordos_ : xVal equal to x[0]
                # if direction is left => x[0][0],x[1][1], right => x[1]
                if direction == "left":
                    coordos = [x[0][0], x[1][1]]
                else:
                    coordos = [x[1][0],x[1][1]]

            return bestRegion

        def diagonal_operation(m, b, startingCoord, gameboardDim, increment = 10**(-5)):

            # increment x
            coordos = [startingCoord[0],startingCoord[1]]
            bestRegion = None
            while coordos[0] <= gameboardDim[0]:
                q = get_best_region_from_horizon(coordos, 'left')
                q2 = get_best_region_from_horizon(coordos, 'right')
                q = comparadantos(q,q2)

                if bestRegion != None:
                    bestRegion = comparadantos(q, bestRegion)
                else:
                    bestRegion = q
                newX = coordos + increment
                newY = newX * m + b
                coordos = (newX,newY)
            return bestRegion

        startCoord = (0, n)
        m, b = FreeAndSimpleScanner.get_diagonal_given_region(((0,0), gameboardDim), diagonal = "down")
        return diagonal_operation(m, b startCoord, gameboardDim)

    ############# END : scanning algorithms

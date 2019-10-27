from copy import deepcopy
from functools import partial
##from AreaScanner import *

## TODO : there is a bug in `calibrate_region_into_square`


class FreeAndSimpleScanner:

    def __init__(self):
        return

    ########## START : methods on coordinates ################

    '''
    description:
    - determines if coordinates denote gameboard dimensions or region

    arguments:
    - coords := (int,int)

    return:
    - gameboard-dim|region
    '''
    @staticmethod
    def get_dimension_format(coords):
        if type(coords[0]) is tuple: return "region"
        return "gameboard-dim"

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

        if not ((coord[0] >= region[0][0] and coord[0] <= region[1][0]) and\
            (coord[1] >= region[0][1] and coord[1] <= region[1][1])):
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
        if tuplePairOfPairs[0][0] > tuplePairOfPairs[1][0] or tuplePairOfPairs[0][1] > tuplePairOfPairs[1][1]:
            tuplePairOfPairs = (tuplePairOfPairs[1], tuplePairOfPairs[0])
        if tuplePairOfPairs[0][0] > tuplePairOfPairs[1][0] or tuplePairOfPairs[0][1] > tuplePairOfPairs[1][1]:
            return False
        return tuplePairOfPairs

    # TODO : test this
    @staticmethod
    def is_region_in_region(r1, r2):
        if not (r1[0][0] >= r2[0][0] and r1[0][0] <= r2[1][0]):
            return False
        if not (r1[0][1] >= r2[0][1] and r1[0][1] <= r2[1][1]):
            return False
        if not (r1[1][0] >= r2[0][0] and r1[1][0] <= r2[1][0]):
            return False
        if not (r1[1][1] >= r2[0][1] and r1[1][1] <= r2[1][1]):
            return False
        return True

    @staticmethod
    def is_square_region(region, rounding = 2):
        m = round(region[1][0], rounding) - round(region[0][0], rounding)
        n = round(region[1][1], rounding) - round(region[0][1], rounding)

        if round(m, rounding) != round(n, rounding):
            return False
        return True

    '''
    description:
    ~

    arguments:
    - region := ((int::(minX), int::(minY)), (int::(maxX), int::(maxY)))

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
            assert type(region) is tuple and len(region) == 2, "invalid region x {}".format(region)
            assert type(region[0]) is tuple and type(region[0]) is type(region[1]), "invalid region y {}".format(region)
            assert (region[1][0] - region[0][0]) >= 0 and (region[1][1] - region[0][1]) >= 0, "invalid region z {}".format(region)
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

    # TODO : check this
    """
    description:
    - makes an increment function using direction

    arguments:
    - direction := left|right|up|down
    - increment := float, negative or positive already set

    return:
    - func((int,int),(int,int)) => (int,int)
    """
    @staticmethod
    def get_increment(gameboardDim, direction, increment):##, mode = "cutoff"):
        increment = FreeAndSimpleScanner.set_increment(gameboardDim, increment)
        if direction == "right":
            ##if mode == "cutoff":
            if FreeAndSimpleScanner.get_dimension_format(gameboardDim) == "gameboard-dim":
                incrementos = lambda c: (c[0] + increment, c[1]) if c[0] + increment \
                        <= gameboardDim[0] else (gameboardDim[0], c[1])
            else:
                incrementos = lambda c: (c[0] + increment, c[1]) if c[0] + increment \
                        <= gameboardDim[1][0] else (gameboardDim[1][0], c[1])
        elif direction == "left":
            if FreeAndSimpleScanner.get_dimension_format(gameboardDim) == "gameboard-dim":
                incrementos = lambda c: \
                    (c[0] + increment, c[1]) if c[0] + increment \
                    >= 0 else (0, c[1])
            else:
                incrementos = lambda c: (c[0] + increment, c[1]) if c[0] + increment \
                        >= gameboardDim[0][0] else (gameboardDim[0][0], c[1])
        elif direction == "up":
            if FreeAndSimpleScanner.get_dimension_format(gameboardDim) == "gameboard-dim":
                incrementos = lambda c: \
                    (c[0], c[1] + increment) if c[1] + increment \
                    <= gameboardDim[1] else (c[0], gameboardDim[1])
            else:
                incrementos = lambda c: (c[0], c[1] + increment) if c[0] + increment \
                        <= gameboardDim[1][1] else (c[0], gameboardDim[1][1])
        else:
            if FreeAndSimpleScanner.get_dimension_format(gameboardDim) == "gameboard-dim":
                incrementos = lambda c: \
                    (c[0], c[1] + increment) if c[1] + increment \
                    >= 0 else (c[0], 0)
            else:
                incrementos = lambda c: (c[0], c[1] + increment) if c[1] + increment \
                        >= gameboardDim[0][1] else (c[0], gameboardDim[0][1])

        return incrementos

    @staticmethod
    def set_increment(gameboardDim, increment = "auto"):
        assert increment == "auto" or type(increment) is float, "invalid increment {}".format(increment)
        # calculate hop automatically by this schematic:
        if increment == "auto":
            if FreeAndSimpleScanner.get_dimension_format(gameboardDim) == "gameboard-dim":
                increment = gameboardDim[0] / 1000
            else:
                increment = (gameboardDim[1][0] - gameboardDim[0][0]) / 1000
        ##else: assert increment >= 0, "invalid increment"
        return increment

    @staticmethod
    def on_border(coord, gameboardDim):
        return True if (coord[0] == gameboardDim[0] or coord[0] == 0)\
            or (coord[1] == gameboardDim[1] or coord[1] == 0) else False

    """
    description:
    - determines if coordinate is on or past border given `direction` of scan.

    arguments:
    - coord := (int,int)
    - targetRegion := ((int::(minX), int::(minY)), (int::(maxX), int::(maxY))::(region))
    - direction := left|right|up|down

    return:
    - bool
    """
    @staticmethod
    def on_border_during_scan_event(coord, targetRegion, direction):
        if direction == "left" and (coord[0] <= targetRegion[0][0] or\
            round(abs(coord[0] - targetRegion[0][0]), 2) == 0): return True

        if direction == "right" and (coord[0] >= targetRegion[1][0] or\
            round(abs(coord[0] - targetRegion[1][0]), 2) == 0):
            #print("TARGET :\t", targetRegion, "\tcoord :\t", coord)
            return True

        if direction == "up" and (coord[1] >= targetRegion[1][1] or\
            round(abs(coord[1] - targetRegion[1][1]), 2) == 0): return True

        if direction == "down" and (coord[1] < targetRegion[0][1] or \
            round(abs(coord[1] - targetRegion[0][1]), 2) == 0): return True

        return False


    """
    description:
    - scans in `direction` until free coordinate found

    arguments:
    - coord := (int,int)
    - gameboardDim := (int,int)|((int,int),(int,int))
    - usedRegions := list(((int::(minX), int::(minY)), (int::(maxX), int::(maxY))))
    - direction := str, left|right|up|down
    - increment := float|auto

    return:
    - (int,int)|False
    """
    @staticmethod
    def line_scan_from_coordinate(coord, gameboardDim, usedRegions, direction = "left", increment = "auto"):
        assert direction in {'left', 'right', 'up', 'down'}, "direction {} invalid".format(direction)
        increment = FreeAndSimpleScanner.set_increment(gameboardDim, increment)

        if direction in {'left', 'down'}:
            increment = -1 * increment

        incrementos = FreeAndSimpleScanner.get_increment(gameboardDim, direction, increment)
        clause = lambda c: True if \
            (c[0] >= 0 and c[0] <= gameboardDim[0]) and\
            (c[1] >= 0 and c[1] <= gameboardDim[1]) else False

        coord_ = coord
        tr = ((0,0),gameboardDim) if FreeAndSimpleScanner.get_dimension_format(gameboardDim) == "gameboard-dim" else gameboardDim
        while clause(coord_):
            if FreeAndSimpleScanner.is_coordinate_free(coord_, usedRegions):
                return coord_

            if FreeAndSimpleScanner.on_border_during_scan_event(coord_, tr, direction):
                break
            coord_ = incrementos(coord_)
            ##print("coord_:\t",coord_)
        return False


    '''
    description:
    - performs line scan starting from a coordinate of type f, shaded or free,
      and scans in direction until extreme(last coordinate in direction)
      coordinate of type f found.

    arguments:
    - coord := (int,int)
    - gameboardDim := (int,int)|((int,int),(int,int))
    - usedRegions := list(((int::(minX), int::(minY)), (int::(maxX), int::(maxY))))
    - regionType := None|free|shaded
    - direction := left|right|up|down
    - increment := int|auto

    return:
    - (int,int)::(maxCoord of regiontype), (int,int)::(minCoord of other regionType)|None
    '''
    @staticmethod
    def line_scan_from_coordinate_for_extreme(coord, gameboardDim, usedRegions, regionType = None, direction = "left", increment = "auto"):
        # get type of region shaded or free
        if regionType is None:
            if FreeAndSimpleScanner.is_coordinate_free(coord, usedRegions):
                regionType = "free"
            else:
                regionType = "shaded"
        assert regionType in {"free", "shaded"}, "invalid regionType {}".format(regionType)

        if regionType == "free":
            clause = lambda c: True if FreeAndSimpleScanner.is_coordinate_free(coord, usedRegions) else False
            ##print("free")
        else:
            clause = lambda c: True if not FreeAndSimpleScanner.is_coordinate_free(coord, usedRegions) else False
            ##print("shade")

        # set increment
        assert direction in {'left', 'right', 'up', 'down'}, "direction {} invalid".format(direction)
        increment = FreeAndSimpleScanner.set_increment(gameboardDim, increment)

        if direction in {'left', 'down'}:
            increment = -1 * increment

        coord_ = coord
        ##print("GD :\t", gameboardDim)
        incrementos = FreeAndSimpleScanner.get_increment(gameboardDim, direction, increment)
        tr = ((0,0),gameboardDim) if FreeAndSimpleScanner.get_dimension_format(gameboardDim) == "gameboard-dim" else gameboardDim
        nextCoord = None


        #### TODO
        #### ATTENTION : there is a possible infinite loop here
        ####                below is a temporary patch
        stall = 0
        maxStall = 10


        while clause(coord):
            coord_ = coord
            ##print("direction :\t", direction)
            ##print("tr :\t", tr)
            if FreeAndSimpleScanner.on_border_during_scan_event(coord_, tr, direction):
                ##print("YES")
                nextCoord = False
                break
            coord = incrementos(coord)
            ##print("bug here :\t{}\tgameboard dim :\t{}".format(coord, gameboardDim))
        if nextCoord is not False: nextCoord = coord
        return coord_, nextCoord

    # not thorough horizontal
    '''
    description:
    - performs a right angle scan starting from some coordinate

    arguments:
    - coord := (int,int)
    - gameboardDim := (int,int)|((int,int),(int,int))
    - usedRegions := list(((int::(minX), int::(minY)), (int::(maxX), int::(maxY)))
    - angleDirectionX := str, left|right
    - angleDirectionY := str, up|down
    - calibrateMode := approximate|square

    return:
    - ((int::(minX), int::(minY)), (int::(maxX), int::(maxY)))|False
    '''
    @staticmethod
    def right_angle_scan_from_coordinate(coord, gameboardDim, usedRegions, angleDirectionX, angleDirectionY, calibrateMode = "approximate", increment = 10**-1):

        assert angleDirectionX in {"left", "right"} and angleDirectionY in \
            {"up", "down"}, "invalid angle directions ({},{})".format(angleDirectionX, angleDirectionY)

        assert calibrateMode in {"approximate", "square"}, "invalid calibrateMode {}".format(calibrateMode)


        ##print("GAMEBOARD DIM:\t", gameboardDim)
        # get max/min values
        coordForX, res = FreeAndSimpleScanner.line_scan_from_coordinate_for_extreme(\
            coord, gameboardDim, usedRegions, "free", angleDirectionX, increment = increment)

        coordForY, res2 =  FreeAndSimpleScanner.line_scan_from_coordinate_for_extreme(\
            coord, gameboardDim, usedRegions, "free", angleDirectionY, increment = increment)

        # determine left bottom corner and right top corner
        xMin, yMin = min(coordForX[0], coord[0]), min(coordForY[1], coord[1])
        xMax, yMax =  max(coordForX[0], coord[0]), max(coordForY[1], coord[1])

        ##print("coordX : {}\tcoordY : {}".format(coordForX, coordForY))
        here = ((xMin, yMin), (xMax, yMax))
        ##print("XXXX :\t" , here)
        if calibrateMode == "square":
            ##print("HEREXXXX:\t", here)
            return AreaScanner.calibrate_region_into_square(here)
        return here

    ############# START : scanning algorithms

    @staticmethod
    def get_overlap_between_regions(r1,r2):
        startX, endX, startY, endY = None, None, None, None

        # determine if minX or maxX in range
        # maxX of r2 is in range of r1
        if r2[1][0] >= r1[0][0] and r2[1][0] <= r1[1][0]:
            startX = min(r2[0][0], r1[0][0])
            endX = r2[1][0]
        # minX of r2 is in range of r1
        elif r2[0][0] >= r1[0][0] and r2[0][0] <= r1[1][0]:
            startX = r2[0][0]
            endX = min(r1[1][0], r2[1][0])
        # maxY of r2 is in range of r1
        elif r2[1][1] >= r1[0][1] and r2[1][1] <= r1[1][1]:
            startY = min(r2[0][0], r1[0][0])
            endY = r2[1][0]
        # minY of r2 is in range of r1
        elif r2[0][1] >= r1[0][1] and r2[0][1] <= r1[1][1]:
            startY = r2[0][0]
            endY = min(r1[1][0], r2[1][0])
        else:
            pass
        return ((startX, startY),(endX,endY)) if startX is not None else None

    ############# END : scanning algorithms


#####################################################################################


"""
description:
- class calculates area of region by incremental approximation
"""
class AreaScanner:

    '''
    description:
    - given two sets of lines
    '''
    @staticmethod
    def get_parallels_between_line_sets(ls1,ls2):
        return -1

    '''
    description:
    - determines if two lines are parallel by comparing slopes

    arguments:
    - l1 := ((int::(minX), int::(minY)), (int::(maxX), int::(maxY)))
    - l2 := ((int::(minX), int::(minY)), (int::(maxX), int::(maxY)))

    return:
    - bool
    '''
    # TODO : test this
    @staticmethod
    def are_lines_parallel(l1, l2):
        # get slopes
        n1 = l1[1][1] - l1[0][1]
        d1 = l1[1][0] - l1[0][0]
        n2 = l2[1][1] - l2[0][1]
        d2 = l2[1][0] - l2[0][0]

        if d1 == 0 and d2 == 0: return True
        if d1 == 0 or d2 == 0: return False
        s1,s2 = n1/d1,n2/d2
        if int(round(abs(s1 -s2),0)) == 0: return True
        return False

    '''
    description:
    - determines if set of lines are parallel

    arguments:
    - l1 := ((int::(minX), int::(minY)), (int::(maxX), int::(maxY)))

    return:
    - bool
    '''
    # TODO : test this
    @staticmethod
    def is_lineset_parallel(lineset):
        if len(lineset) == 0: return False
        q = list(lineset)
        x = lineset[0]

        for i in range(1, len(lineset)):
            if not AreaScanner.are_lines_parallel(lineset[i], x):
                return False
        return True


    '''
    description:
    - this method is a helper for area-scanning, each of these two linesets
      belong to a horizontal line.
    - method does not have error-checking codes

    arguments:
    - ls1 := set(((int::(minX), int::(minY)), (int::(maxX), int::(maxY))))
    - ls2 := set(((int::(minX), int::(minY)), (int::(maxX), int::(maxY))))

    return:
    - list((int::(xMin), int::(xMax)))
    '''
    @staticmethod
    def get_horizontal_coexistence_between_linesets(ls1, ls2):
        # sort linesets
        # iterate through 1 and check

        ci1 = 0
        ci2 = 0 # current index for lineset 2
        coexistence = []

        while ci1 < len(ls1) and ci2 < len(ls2):
            x1 = ls1[ci1]

            # increment ci2 until minX is greater than maxX of x1
            while ci2 < len(ls2):
                x2 = ls2[ci2]
                if x2[0][0] >= x1[1][0]: # increment ci1
                    ci1 += 1
                    break
                # determine if any minX of ls2 found in x
                if x2[0][0] >= x1[0][0] and x2[0][0] <= x1[1][0]:
                    minX = x2[0][0]
                    maxX = min(x1[1][0], x2[1][0])
                    ##coexistence.add((minX, maxX))
                    coexistence.append((minX, maxX))
                # any maxX of ls2 found in x
                elif x1[0][0] >= x2[0][0] and x1[0][0] <= x2[1][0]:
                    minX = x1[0][0]
                    maxX = min(x1[1][0], x2[1][0])
                    ##coexistence.add((minX, maxX))
                    coexistence.append((minX, maxX))

                ci2 += 1
        return coexistence

    #---------------------

    """
    description:
    - calculates the range of a free or shaded line starting from `startCoord`

    arguments:
    - startCoord := (int,int)
    - gameboardDim := (int,int)|((int,int),(int,int))
    - usedRegions := list(((int::(minX), int::(minY)), (int::(maxX), int::(maxY))))
    - direction := left|right|up|down
    - increment := auto|float

    return:
    - list(((int::(minX), int::(minY)), (int::(maxX), int::(maxY)))), linesets
    - (int,int)|False, last coordinate
    """
    @staticmethod
    def scan_collect_free_lineset_(startCoord, gameboardDim, usedRegions, direction = "right", increment = 10 **(-3)):
        startPoint1 = (0, 1.5)
        freeLineSegments = [] # ((minX,minY), (maxX, maxY))
        regionType = "free" if FreeAndSimpleScanner.is_coordinate_free(startCoord, usedRegions) else "shaded"
        tr = ((0,0),gameboardDim) if FreeAndSimpleScanner.get_dimension_format(gameboardDim) == "gameboard-dim" else gameboardDim
        clause = lambda c: False if FreeAndSimpleScanner.on_border_during_scan_event(c, tr, direction) else True

        coord = startCoord
        lineset = []
        while clause(coord):
            q1, q2 = FreeAndSimpleScanner.line_scan_from_coordinate_for_extreme(coord, gameboardDim, usedRegions,\
                regionType, direction)
            ##print("q11:\t", q1)
            ##print("scan right:\t", q2)
            if regionType == "free":
                x = FreeAndSimpleScanner.to_proper_region((coord, q1))
                lineset.append(x)
                regionType = "shaded"
            else: regionType = "free"
            coord = q2
            if q2 == False:
                break
        return lineset, coord

    """
    description:
    ~ see method above

    return:
    - list(((int::(minX), int::(minY)), (int::(maxX), int::(maxY)))), linesets
    """
    # TODO : error here
    @staticmethod
    def scan_collect_free_lineset(startCoord, gameboardDim, usedRegions, direction = "right", increment = 10 **(-2)):
        tr = ((0,0),gameboardDim) if FreeAndSimpleScanner.get_dimension_format(gameboardDim) == "gameboard-dim" else gameboardDim
        clause = lambda c: False if FreeAndSimpleScanner.on_border_during_scan_event(c, tr, direction = direction) else True
        lineset = []
        coord = startCoord
        while clause(coord):
            ls, coord = AreaScanner.scan_collect_free_lineset_(coord, tr, usedRegions, direction, increment)
            lineset.extend(ls)
            ##print("coord:\t", coord)
            if coord == False: break
        return lineset

    ####################################################

    ####################################################

    '''
    description:
    - calculates area given a list of (minX,maxX) info. for listOfSegments

    arguments:
    - listOfSegments := list((minX,maxX))

    return:
    - float
    '''
    @staticmethod
    def get_area_from_horizontal_line_segments(listOfSegments, increment):
        # get the total length
        c = sum([l[1] - l[0] for l in listOfSegments])
        return c * increment

    '''
    description:
    - calculates approximate area of `wantedRegion`

    arguments:
    - wantedRegion := ((int::(minX), int::(minY)), (int::(maxX), int::(maxY)))
    - usedRegions := list(((int::(minX), int::(minY)), (int::(maxX), int::(maxY))))
    - increment := float

    return:
    - float
    '''
    @staticmethod
    def sloppy_area_scan(wantedRegion, usedRegions, increment = 10**(-2)):
        ##print("X")
        ##("f", FreeAndSimpleScanner)
        if wantedRegion == None: return False ##### ?? TODO
        assert FreeAndSimpleScanner.is_proper_region(wantedRegion) is True, "invalid region {}".format(wantedRegion)
        if FreeAndSimpleScanner.get_area_of_region(wantedRegion) == 0:
            return False

        ##print("SS")
        # scan from lower left corner to upper right corner
        startCoord = wantedRegion[0]
        ##print("START:\t",startCoord)
        clause = lambda c: False if FreeAndSimpleScanner.on_border_during_scan_event(c, wantedRegion, direction = "up") else True
        incrementos = FreeAndSimpleScanner.get_increment(wantedRegion, "up", increment)
        totalArea = 0
        ls1,ls2 = None, None
        ##allLineSets = []
        ##print("SS :\t", startCoord)
        ##print("free")

        while clause(startCoord):
            ls2 = ls1

            ls1 = AreaScanner.scan_collect_free_lineset(startCoord, wantedRegion, usedRegions,\
                direction = "right", increment = increment)
            ##print("free ls:\t",ls1)

            ##allLineSets.append(ls1)
            if ls1 != None and ls2 != None:
                coex = AreaScanner.get_horizontal_coexistence_between_linesets(ls1, ls2)
                a = AreaScanner.get_area_from_horizontal_line_segments(coex, increment)
                totalArea += a
            startCoord = incrementos(startCoord)
            ##print("A NOW :\t", totalArea)
            #print("SC:\t",startCoord)
        return totalArea##, ls1

    # TODO : check this
    """
    description:
    - to be used with multiprocessing
    """
    @staticmethod
    def sloppy_area_scan_(usedRegions, increment, wantedRegion):
        a = AreaScanner.sloppy_area_scan(wantedRegion, usedRegions, increment)
        return wantedRegion, a

    @staticmethod
    def get_area_from_coordinate_pairs(wantedRegion, usedRegions, increment, p):
        p1, p2 = p

        ls1 = AreaScanner.scan_collect_free_lineset(p1, wantedRegion, usedRegions,\
            direction = "right", increment = increment)
        ls2 = AreaScanner.scan_collect_free_lineset(p2, wantedRegion, usedRegions,\
            direction = "right", increment = increment)

        coex = AreaScanner.get_horizontal_coexistence_between_linesets(ls1, ls2)
        area = AreaScanner.get_area_from_horizontal_line_segments(coex, increment)
        return area

    '''
    description:
    -

    arguments:
    - coord := (int,int), a free coordinate given `usedRegions`
    '''
    @staticmethod
    def get_best_region_given_coordinates(coord, gameboardDim, usedRegions, increment = 10**(-2), calibrateMode = "square"):

        tr = ((0,0),gameboardDim) if FreeAndSimpleScanner.get_dimension_format(gameboardDim) == "gameboard-dim" else gameboardDim
        ##print("TR:\t",tr)
        if FreeAndSimpleScanner.get_area_of_region(tr) == 0:
            return False

        ##print("USED:\t", usedRegions)

        # get 4 regions
        lu = FreeAndSimpleScanner.right_angle_scan_from_coordinate(coord, tr, usedRegions, "left", "up", calibrateMode = calibrateMode)
        ld = FreeAndSimpleScanner.right_angle_scan_from_coordinate(coord, tr, usedRegions, "left", "down", calibrateMode = calibrateMode)
        ru = FreeAndSimpleScanner.right_angle_scan_from_coordinate(coord, tr, usedRegions, "right", "up", calibrateMode = calibrateMode)
        rd = FreeAndSimpleScanner.right_angle_scan_from_coordinate(coord, tr, usedRegions, "right", "down", calibrateMode = calibrateMode)

        ##
        """
        print("lu:\t", lu)
        print("ld:\t", ld)
        print("ru:\t", ru)
        print("rd:\t", rd)
        """
        ##
        ##print("USED R :\t", usedRegions)
        d = {}
        if lu != False:
            a = AreaScanner.sloppy_area_scan(lu, usedRegions, increment = increment)
            if a != False:
                d[lu] = a
        if ld != False:
            a = False
            a = AreaScanner.sloppy_area_scan(ld, usedRegions, increment = increment)
            if a != False:
                d[ld] = a
        if ru != False:
            ##print("RU :\t", ru, "\tusedR :\t", usedRegions)
            a = False
            a = AreaScanner.sloppy_area_scan(ru, [], increment = increment)
            ##print("HERE A:\t", a)
            if a != False:
                d[ru] = a

        if rd !=False:
            a = False
            a = AreaScanner.sloppy_area_scan(rd, usedRegions, increment = increment)
            if a != False:
                d[rd] = a

        ##print("DDDD :\t",d)
        #print("HERE :\")
        # sort dictionary by
        d = sorted(d.items(), key=lambda kv: kv[1])
        return d[-1] if len(d) > 0 else False

    ## TODO : untested
    ## wacky function
    '''
    description:
    - determines a best corner to fit `wantedDimensions` into `targetRegion` given `usedRegions`
    - call this the `corner fit` algorithm.

    arguments:
    - wantedDimensions := (int,int)
    - targetRegion := ((int::(minX), int::(minY)), (int::(maxX), int::(maxY)))
    - gameboardDim := (int,int)
    - usedRegions := list(((int::(minX), int::(minY)), (int::(maxX), int::(maxY))))

    return:
    -

    '''
    @staticmethod
    def get_best_region_fit_given_target_region(wantedDimensions, targetRegion, gameboardDim, usedRegions):

        ## wrong
        assert wantedDimensions[0] <= gameboardDim[0] and wantedDimensions[1] <= gameboardDim[1], "invalid : wanted dimensions {} game dimensions {}".format(wantedDimensions, gameboardDim)

        # gameboard dimensions for each must take into account wantedDimensions

        # right up : bottom left corner of targetRegion
        gd = (targetRegion[0], (targetRegion[0] + wantedDimensions[0],\
            targetRegion[1] + wantedDimensions[1]))
        ru = AreaScanner.get_best_region_given_coordinates(targetRegion[0], gd, usedRegions, increment = 10**(-2))
        ##print("ONE :\t", ru)

        # right down : upper left corner of targetRegion
        gd = ((targetRegion[0][0], targetRegion[1][1] - wantedDimensions[1]),\
            (targetRegion[0][0] + wantedDimensions[0], targetRegion[1][1]))
        rd = AreaScanner.get_best_region_given_coordinates((gd[0][0], gd[1][1]), gd, usedRegions, increment = 10**(-2))

        # left up : bottom right corner of targetRegion
        gd = ((targetRegion[1][0] - wantedDimensions[0], targetRegion[0][1]),\
            (targetRegion[1][0], targetRegion[0][1] + wantedDimensions[1]))
        lu = AreaScanner.get_best_region_given_coordinates((gd[1][0], gd[0][1]), gd, usedRegions, increment = 10**(-2))

        # left down : upper right corner of targetRegion
        gd = ((targetRegion[1][0] - wantedDimensions[0], targetRegion[1][1] - wantedDimensions[1]),\
            targetRegion[1])
        ld = AreaScanner.get_best_region_given_coordinates(gd[1], gd, usedRegions, increment = 10**(-2))

        # sort for greatest area
        d = {}
        x = [ru,rd,lu,ld]
        for x_ in x:
            if x_[1] != False: d[x_[0]] = x_[1]
        d = sorted(d.items(), key=lambda kv: kv[1])
        return d[-1] if len(d) > 0 else False

    '''
    description:
    - calibrates region into a square starting from bottom-left

    arguments:
    - new := `region`

    return:
    - `region`
    '''
    @staticmethod
    def calibrate_region_into_square(new):
        d1, d2 = new[1][0] - new[0][0] , new[1][1] - new[0][1]
        if round(abs(d1 -d2), 0) != 0:
            m = min(d1, d2)
            new_ = (tuple(new[0]), (new[0][0] + m, new[0][1] + m))
            return new_
        return new

    # TODO : test this
    """
    description:
    - calibrates a wantedRegion so that it stays inside

    arguments:
    - wantedRegion := ((int,int),(int,int))
    - gameboardDim := (int,int)
    - calibrateMode := `square`|`approximate`

    return:
    - `region`
    """
    @staticmethod
    def calibrate_wanted_region_given_gameboard_dimensions(wantedRegion, gameboardDim, calibrateMode = "approximate"):
        assert calibrateMode in {"approximate", "square"}, "invalid calibrateMode {}".format(calibrateMode)
        new = [list(wantedRegion[0]), list(wantedRegion[1])]


        q = []
        if wantedRegion[0][0] < 0:
            new[0][0] = 0
            if calibrateMode == "square":
                diff = wantedRegion[1][0] - wantedRegion[0][0]
                newXDimMin = diff + wantedRegion[0][0]
                q.append(newXDimMin)
        if wantedRegion[0][1] < 0:
            new[0][1] = 0
            if calibrateMode == "square":
                diff = wantedRegion[1][1] - wantedRegion[0][1]
                newYDimMin = diff + wantedRegion[0][1]
                q.append(newYDimMin)
        if wantedRegion[1][0] > gameboardDim[0]:
            new[1][0] = gameboardDim[0]
            if calibrateMode == "square":
                diff = wantedRegion[1][0] - gameboardDim[0]
                newXDimMax = (wantedRegion[1][0] - wantedRegion[0][0]) - diff
                q.append(newXDimMax)
        if wantedRegion[1][1] > gameboardDim[1]:
            new[1][1] = gameboardDim[1]
            if calibrateMode == "square":
                diff = wantedRegion[1][1] - gameboardDim[1]
                newYDimMax = (wantedRegion[1][1] - wantedRegion[0][1]) - diff
                q.append(newYDimMax)

        ##print("calibrating :\t")
        out = (tuple(new[0]), tuple(new[1]))

        if calibrateMode == "approximate":
            return out

        if len(q) == 0:
            return out

        x = min(q)
        out = (out[0], (out[0][0] + x, out[0][1] + x))
        ##print("OUT:\t", out)
        return out

    # TODO : test this for square calibration
    """
    description:
    - sometimes, there are no squares but still regions nonetheless


    arguments:
    - coord := (int,int)
    - gameboardDim := (int,int)|((int,int),(int,int))
    - wantedDimensions :=  (int,int)
    - usedRegions := list(`region`)
    - increment := float
    - calibrateMode := approximate|square
                approximate is if select region for check can be size other than wantedDimensions
                exact is if select region for check has to be size wantedDimensions

    return:
    - (`region`, `approximate free area`)
    """
    @staticmethod
    def get_best_region_fit_given_wanted_dimensions(coord, gameboardDim, wantedDimensions, usedRegions, increment = 10**(-1), calibrateMode = "approximate"):
        assert wantedDimensions[0] <= gameboardDim[0] and wantedDimensions[1] <= gameboardDim[1], "invalid : wanted dimensions {} game dimensions {}".format(wantedDimensions, gameboardDim)
        assert wantedDimensions[0] > 0 and wantedDimensions[1] > 0, "invalid wantedDimensions {}".format(wantedDimensions)
        ##print("wanted dim :\t", wantedDimensions)

        # right up : coord is (minX, minY)
        gd =  (coord, (coord[0] + wantedDimensions[0], coord[1] + wantedDimensions[1]))
        gd = AreaScanner.calibrate_wanted_region_given_gameboard_dimensions(gd, gameboardDim, "square")
        ##print("ru :\t", gd)
        ru = AreaScanner.get_best_region_given_coordinates(coord, gd, usedRegions, increment = increment)
        ##print("ru2 :\t", ru)

        # right down : coord[0] is minX
        gd =  ((coord[0], coord[1] - wantedDimensions[1]), (coord[0] + wantedDimensions[0], coord[1]))
        gd = AreaScanner.calibrate_wanted_region_given_gameboard_dimensions(gd, gameboardDim, "square")
        ##print("rd :\t", gd)
        rd = AreaScanner.get_best_region_given_coordinates(coord, gd, usedRegions, increment = increment)

        # left up : coord is bottom right
        gd = ((coord[0] - wantedDimensions[0], coord[1]), (coord[0], coord[1] + wantedDimensions[1]))
        gd = AreaScanner.calibrate_wanted_region_given_gameboard_dimensions(gd, gameboardDim, "square")
        ##print("lu :\t", gd)
        lu = AreaScanner.get_best_region_given_coordinates(coord, gd, usedRegions, increment = increment)

        # left down : coord is top right
        gd = ((coord[0] - wantedDimensions[0], coord[1] - wantedDimensions[1]), coord)
        ##print("before :\t", gd)
        gd = AreaScanner.calibrate_wanted_region_given_gameboard_dimensions(gd, gameboardDim, "square")
        ##print("ld :\t", gd)
        ld = AreaScanner.get_best_region_given_coordinates(coord, gd, usedRegions, increment = increment)

        # sort for greatest area
        d = {}
        x = [ru,rd,lu,ld]

        ##for x_ in x: print("here xxx :\t",x_)

        ##print("HERE0:\t", x)

        for x_ in x:
            if x_ != False:
                ##d[x_[0]] = FreeAndSimpleScanner.get_area_of_region(x_[0])
                ##print("YES :\t", x_)
                d[x_[0]] = x_[1]

        ##print("D HERE :\t", d)

        d = sorted(d.items(), key=lambda kv: kv[1])
        x = d[-1] if len(d) > 0 else False
        ##print("HERE :\t", x)
        return x

from FreeAndSimpleScanner import *

# TODO : for target area
#- mode := (max::())|(fit::())

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
            print("q11:\t", q1)
            print("scan right:\t", q2)
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
    @staticmethod
    def scan_collect_free_lineset(startCoord, gameboardDim, usedRegions, direction = "right", increment = 10 **(-2)):
        tr = ((0,0),gameboardDim) if FreeAndSimpleScanner.get_dimension_format(gameboardDim) == "gameboard-dim" else gameboardDim
        #clause = lambda c: False if FreeAndSimpleScanner.on_border_during_scan_event(c, tr, direction = direction) else True
        lineset = []
        coord = startCoord
        while coord != False:
            ls, coord = AreaScanner.scan_collect_free_lineset_(coord, tr, usedRegions, direction, increment)
            lineset.extend(ls)
            print("yes")
        return lineset

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
        assert FreeAndSimpleScanner.is_proper_region(wantedRegion) is True, "invalid region {}".format(wantedRegion)

        '''
        description:
        - calculates area given a list of (minX,maxX) info. for listOfSegments

        arguments:
        - listOfSegments := list((minX,maxX))

        return:
        - float
        '''
        def get_area_from_horizontal_line_segments(listOfSegments, increment):
            # get the total length
            c = sum([l[1] - l[0] for l in listOfSegments])
            ##print("c\t",c)
            return c * increment

        # scan from lower left corner to upper right corner
        startCoord = wantedRegion[0]
        ##print("START:\t",startCoord)
        clause = lambda c: False if FreeAndSimpleScanner.on_border_during_scan_event(c, wantedRegion, direction = "up") else True
        incrementos = FreeAndSimpleScanner.get_increment(wantedRegion, "up", increment)
        totalArea = 0
        ls1,ls2 = None, None
        allLineSets = []

        while clause(startCoord):
            ls2 = ls1

            ls1 = AreaScanner.scan_collect_free_lineset(startCoord, wantedRegion, usedRegions,\
                direction = "right", increment = 10 **(-3))
            allLineSets.append(ls1)
            if ls1 != None and ls2 != None:
                coex = AreaScanner.get_horizontal_coexistence_between_linesets(ls1, ls2)
                a = get_area_from_horizontal_line_segments(coex, increment)
                totalArea += a
            startCoord = incrementos(startCoord)
        return totalArea, ls1

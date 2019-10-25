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
            return c * increment

        print("SS")

        # scan from lower left corner to upper right corner
        startCoord = wantedRegion[0]
        ##print("START:\t",startCoord)
        clause = lambda c: False if FreeAndSimpleScanner.on_border_during_scan_event(c, wantedRegion, direction = "up") else True
        incrementos = FreeAndSimpleScanner.get_increment(wantedRegion, "up", increment)
        totalArea = 0
        ls1,ls2 = None, None
        ##allLineSets = []
        print("SS :\t", startCoord)
        print("free")

        while clause(startCoord):
            ls2 = ls1

            ls1 = AreaScanner.scan_collect_free_lineset(startCoord, wantedRegion, usedRegions,\
                direction = "right", increment = 10 **(-3))
            #print("free ls:\t",ls1)

            ##allLineSets.append(ls1)
            if ls1 != None and ls2 != None:
                coex = AreaScanner.get_horizontal_coexistence_between_linesets(ls1, ls2)
                a = get_area_from_horizontal_line_segments(coex, increment)
                totalArea += a
            startCoord = incrementos(startCoord)
            #print("SC:\t",startCoord)
        return totalArea##, ls1

    '''
    description:
    -

    arguments:
    - coord := (int,int), a free coordinate given `usedRegions`
    '''
    @staticmethod
    def get_best_region_given_coordinates(coord, gameboardDim, usedRegions, increment = 10**(-2)):

        if FreeAndSimpleScanner.get_area_of_region(((0,0),gameboardDim)) == 0:
            return False

        print("YES")


        # get 4 regions
        lu = FreeAndSimpleScanner.right_angle_scan_from_coordinate(coord, gameboardDim, usedRegions, "left", "up")
        ld = FreeAndSimpleScanner.right_angle_scan_from_coordinate(coord, gameboardDim, usedRegions, "left", "down")
        ru = FreeAndSimpleScanner.right_angle_scan_from_coordinate(coord, gameboardDim, usedRegions, "right", "up")
        rd = FreeAndSimpleScanner.right_angle_scan_from_coordinate(coord, gameboardDim, usedRegions, "right", "down")

        ##
        """
        print("lu:\t", lu)
        print("ld:\t", ld)
        print("ru:\t", ru)
        print("rd:\t", rd)
        """
        ##

        d = {}
        if lu != False:
            d[lu] = AreaScanner.sloppy_area_scan(lu, usedRegions, increment = increment)
        if ld != False:
            d[ld] = AreaScanner.sloppy_area_scan(ld, usedRegions, increment = increment)
        if ru != False:
            d[ru] = AreaScanner.sloppy_area_scan(ru, usedRegions, increment = increment)
        if rd !=False:
            d[rd] = AreaScanner.sloppy_area_scan(rd, usedRegions, increment = increment)

        # sort dictionary by
        ##print("HERE:\t",d)
        d = sorted(d.items(), key=lambda kv: kv[1])
        #return d
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

    # TODO : test this
    @staticmethod
    def calibrate_wanted_region_given_gameboard_dimensions(wantedRegion, gameboardDim):
        new = [list(wantedRegion[0]), list(wantedRegion[1])]
        if wantedRegion[0][0] < 0:
            new[0][0] = 0
        if wantedRegion[0][1] < 0:
            new[0][1] = 0
        if wantedRegion[1][0] > gameboardDim[0]:
            new[1][0] = gameboardDim[0]
        if wantedRegion[1][1] > gameboardDim[1]:
            new[1][1] = gameboardDim[1]
        return new


    """
    description:
    -
    """
    @staticmethod
    def get_best_region_fit_given_wanted_dimensions(coord, gameboardDim, wantedDimensions, usedRegions, increment = 10**(-2)):
        assert wantedDimensions[0] <= gameboardDim[0] and wantedDimensions[1] <= gameboardDim[1], "invalid : wanted dimensions {} game dimensions {}".format(wantedDimensions, gameboardDim)

        # right up : coord is (minX, minY)
        gd =  (coord, (coord[0] + wantedDimensions[0], coord[1] + wantedDimensions[1]))
        gd = AreaScanner.calibrate_wanted_region_given_gameboard_dimensions(gd, gameboardDim)
        ru = AreaScanner.get_best_region_given_coordinates(coord, gd, usedRegions, increment = 10**(-2))

        # right down : coord[0] is minX
        gd =  ((coord[0], coord[1] - wantedDimensions[1]), (coord[0] + wantedDimensions[0], coord[1]))
        gd = AreaScanner.calibrate_wanted_region_given_gameboard_dimensions(gd, gameboardDim)
        rd = AreaScanner.get_best_region_given_coordinates(coord, gd, usedRegions, increment = 10**(-2))

        # left up : coord is bottom right
        gd = ((coord[0] - wantedDimensions[0], coord[1]), (coord[0], coord[1] + wantedDimensions[1]))
        gd = AreaScanner.calibrate_wanted_region_given_gameboard_dimensions(gd, gameboardDim)
        lu = AreaScanner.get_best_region_given_coordinates(coord, gd, usedRegions, increment = 10**(-2))

        # left down : coord is top right
        gd = ((coord[0] - wantedDimensions[0], coord[1] - wantedDimensions[1]), coord)
        gd = AreaScanner.calibrate_wanted_region_given_gameboard_dimensions(gd, gameboardDim)
        ld = AreaScanner.get_best_region_given_coordinates(coord, gd, usedRegions, increment = 10**(-2))

        # sort for greatest area
        d = {}
        x = [ru,rd,lu,ld]
        for x_ in x:

            if x_ != False: d[x_[0]] = x_[1]
        d = sorted(d.items(), key=lambda kv: kv[1])
        return d[-1] if len(d) > 0 else False

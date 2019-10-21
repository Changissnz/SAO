"""
description:
- a scanner to scan for space, if only to see the free space.
"""
class FreeAndSimpleScanner:

    def __init__(self):
        return

    ############# START : scanner analytics go here
    @staticmethod
    def get_region_area_unused(targetRegion, usedRegions):
        return -1

    @staticmethod
    def is_nonnegative_coordinate(coord):
        return True if coord[0] >= 0 and coord[1] >= 0 else False

    '''
    description:
    ~

    arguments:
    - region := ((int::(minX), int::(minY)), (int::(maxX), int::(maxY))::(region)) | False

    return:
    - float
    '''
    @staticmethod
    def get_area_of_region(region):
        if not FreeAndSimpleScanner.is_proper_region(region):
            return False
        m = abs(region[1][0] - region[0][0])
        n = abs(region[1][1] - region[0][1])
        return m * n

    @staticmethod
    def is_proper_region(region):
        try:
            assert type(region) is tuple and len(region) is 2, "invalid region {}".format(region)
            assert type(region[0]) is tuple and type(region[0]) is type(region[1]), "invalid region {}".format(region)
            assert len(region[0]) == 2 and type(region[0]) == 2, "invalid region {}".format(region)
            ##assert (region[1][0] - region[0][0]) >= 0 and (region[1][1] - region[0][1]) >= 0, "invalid region {}".format(region)
            return True
        except: return False

    ############# END : scanner analytics go here

    @staticmethod
    def get_slope_given_dimensions(dimensions):
        assert (dimensions[0] != 0 or dimensions[0] != 0), "dimensions cannot be zero, this is the real 2-d world"
        # get m
        return dimensions[1] / dimensions[0]

    # set b initially to y

    '''
    description:
    - this is to scan right and down for region at this point in downward-incrementation.

    arguments:
    - slope := int, slope-value for slope formula
    - b := int, b-value for slope formula
    - gameboardDim := (int::(x), int::(y))
    - usedRegions := list((int::(minX), int::(minY)), (int::(maxX), int::(maxY))::(region))
    - sufficiencyRequirement := float, minimum area requirement for region

    return:
    - ((int::(minX), int::(minY)), (int::(maxX), int::(maxY))::(region)) | False
    '''
    @staticmethod
    def increment_one_down_and_scan_for_region(slope, b, gameboardDim, usedRegions, hop = "auto", sufficiencyRequirement = "auto"):
        assert sufficiencyRequirement == "auto" or type(sufficiencyRequirement) is float, "invalid sufficiencyRequirement {}".format(sufficiencyRequirement)
        if type(sufficiencyRequirement) is float:
            assert sufficiencyRequirement >= 0 and sufficiencyRequirement <= gameboardDim[0] * gameboardDim[1], "invalid sufficiencyRequirement {}".format(sufficiencyRequirement)
        assert hop == "auto" or type(hop) is float, "invalid hop {}".format(hop)

        if hop == "auto":
            hop = gameboardDim[0] / 1000

        if sufficiencyRequirement == "auto":
            sufficiencyRequirement = (gameboardDim[0] * gameboardDim[1]) / 1000

        # scan will go from x_ = 0 to x_ = m
        newB = b + scanIncrement
        x_ = 0
        while x_ <= boardDimensions[0]:
            q = slope * x_
            newY = q + newB
            coord = (x_, newY)

            # x, and y must be non-negative
            if not FreeAndSimpleScanner.is_nonnegative_coordinate(coord):
                x_ += hop
                continue

            if FreeAndSimpleScanner.coordinate_is_free(coord):
                r = FreeAndSimpleScanner.find_region_from_coord(coord, gameboardDim, usedRegions, direction = "down")
                area = FreeAndSimpleScanner.get_area_of_region(r)
                if area >= sufficiencyRequirement:
                    return r
            x_ += hop
        return False

    '''
    description:
    - find region from coord by directionality up or down

    arguments:
    - coord := (int::(x), int::(y))
    - direction := up|down

    return:
    - (int::(minX), int::(minY)), (int::(maxX), int::(maxY))
    '''
    @staticmethod
    def find_region_from_coord(coord, gameboardDim, usedRegions, direction = "down"):
        assert direction in {"up", "down"}, "direction {} invalid".format(direction)
        currentCoord = deepcopy(coord)
        if direction == "down":
            mode = "max"
        else:
            mode = "min"

        # scan right and down
        ## scan right
        newX = FreeAndSimpleScanner.sloppy_scan(currentCoord, gameboardDim, usedRegions, hop = "auto", mode = "max", scanDirection = "horizontal")
        ## scan down
        newY = FreeAndSimpleScanner.sloppy_scan(currentCoord, gameboardDim, usedRegions, hop = "auto", mode = "max", scanDirection = "vertical")
        return (currentCoord, (newX, newY))

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
        assert type(region) is tuple and len(region) == 2, "invalid region"
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


    @staticmethod
    def sloppy_scan(coord, gameboardDim, usedRegions, hop = "auto", mode = "max", scanDirection = "horizontal"):
        ##newX = sloppy_scan_horizontal(currentCoord, hop = "auto", mode = mode)
        assert hop == "auto" or type(hop) is float, "invalid hop {}".format(hop)
        assert mode in {"min", "max"}, "invalid mode {}".format(mode), "sdf"
        assert scanDirection in {"horizontal", "vertical"}, "scanDirection {} invalid".format(scanDirection)

        # calculate hop automatically by this schematic:
        if hop == "auto":
            hop = gameboardDim[0] / 1000

        currentCoord = [coord[0],coord[1]]
        incrementia = hop

        if mode == "max":
            threshold = gameboardDim[0] if scanDirection == "horizontal" else gameboardDim[1]
            funko = lambda c : True if c[0] <= threshold else False
        else:
            threshold = 0
            funko = lambda c : True if c[0] >= threshold else False
            incrementia = -1 * hop

        while funko(currentCoord):
            if not FreeAndSimpleScanner.is_coordinate_free(currentCoord, usedRegions):
                break
            if scanDirection == "horizontal": currentCoord[0] += incrementia
            else: currentCoord[1] += incrementia

        return currentCoord[0] if scanDirection == "horizontal" else currentCoord[1]

from FreeAndSimpleScanner import *
import unittest

class FreeAndSimpleScannerMethodsTest(unittest.TestCase):

    def test_FreeAndSimpleScanner_IsInRegion(self):
        coord = (2, 2)
        region1 = ((0, 0), (2.1, 2.0))
        region2 = ((0, 0), (2.1, 1.9)) # fail
        region3 = ((1.5, 2.2), (1.9, 2.3)) # fail
        region4 = ((1.9, 1.9), (2.2, 2.4))

        self.assertTrue(FreeAndSimpleScanner.is_in_region(coord, region1))
        self.assertFalse(FreeAndSimpleScanner.is_in_region(coord, region2))
        self.assertFalse(FreeAndSimpleScanner.is_in_region(coord, region3))
        self.assertTrue(FreeAndSimpleScanner.is_in_region(coord, region4))

    def test_FreeAndSimpleScanner_ToProperRegion(self):

        region1 = ((0, 0), (2,2))
        region2 = ((12, 14), (6, 20)) # fail
        region3 = ((4,4), (3, 3))
        region4 = ((12, 17), (18, 12)) # fail

        self.assertTrue(FreeAndSimpleScanner.to_proper_region(region1))
        self.assertFalse(FreeAndSimpleScanner.to_proper_region(region2))
        self.assertTrue(FreeAndSimpleScanner.to_proper_region(region3))
        self.assertFalse(FreeAndSimpleScanner.to_proper_region(region4))

    def test_FreeAndSimpleScanner_GetDiagonalGivenRegion(self):

        # test variables
        region1 = ((0, 0), ((4, 3)))
        r1D = (-3/4, 3)
        r1U = (3/4, 0)


        region2 = ((1,2), (4,15))
        r2U = ((15-2)/(4-1), 15 - (15-2)/(4-1) * 4)
        r2D = ((15-2)/(1-4), 15 - ((15-2)/(1-4) *1))


        # get diagonals
        diag1D = FreeAndSimpleScanner.get_diagonal_given_region(region1, diagonal = "down")
        diag1U = FreeAndSimpleScanner.get_diagonal_given_region(region1, diagonal = "up")
        diag2D = FreeAndSimpleScanner.get_diagonal_given_region(region2, diagonal = "down")
        diag2U = FreeAndSimpleScanner.get_diagonal_given_region(region2, diagonal = "up")


        # test downwards
        self.assertTrue(FreeAndSimpleScannerMethodsTest.is_equal_rounded(diag1D, r1D))
        self.assertTrue(FreeAndSimpleScannerMethodsTest.is_equal_rounded(diag1U, r1U))
        self.assertTrue(FreeAndSimpleScannerMethodsTest.is_equal_rounded(diag2D, r2D))
        self.assertTrue(FreeAndSimpleScannerMethodsTest.is_equal_rounded(diag2U, r2U))

    @staticmethod
    def Sample_Args():

        # used regions
        gameboardDim = (2,2)
        startPoint = (1,1)

        usedRegionLeft = ((0,0.5),(0.5,1.5))
        usedRegionRight = ((0,0.5),(0.5,1.5))
        usedRegionUp = ((0,0.5),(0.5,1.5))
        usedRegionDown = ((0,0.5),(0.5,1.5))

        return {"gameboardDim":gameboardDim,
                "usedRegions": [usedRegionLeft, usedRegionRight, usedRegionUp, usedRegionDown]
                }

    # TODO : check this.
    def test_FreeAndSimpleScanner_LineScanFromCoordinate(self):
        # test case 1
        gameboardDim = (3,3)
        usedRegions = [((0.5,0), (1.5,3))]

        # test scan
        ## scan right tests
        startPoint1 = (0, 1.5)
        q1 = FreeAndSimpleScanner.line_scan_from_coordinate(startPoint1,\
            gameboardDim, usedRegions, direction = "right", increment = "auto")
        print("scan right at {} : {}".format(startPoint1, q1))
        #self.assertTrue(q1 == startPoint1, "error: right test start {} : got {}".format(startPoint1, q1))

        startPoint2 = (1, 1.5)
        q2 = FreeAndSimpleScanner.line_scan_from_coordinate(startPoint2,\
            gameboardDim, usedRegions, direction = "right", increment = "auto")
        print("scan right at {} : {}".format(startPoint2, q2))
        d1, d2 = abs(q2[0] - 1.5), 1.5
        #self.assertTrue(d1 <= 9 / 1000 and d2 == q2[1],"error: right test start {} : got {}".format(startPoint2, q2))

        startPoint3 = (2.5, 2.5)
        q3 = FreeAndSimpleScanner.line_scan_from_coordinate(startPoint3,\
            gameboardDim, usedRegions, direction = "right", increment = "auto")
        print("scan right at {} : {}".format(startPoint3, q3))
        #self.assertTrue(q3 == startPoint3, "error: right test start {} : got {}".format(startPoint3, q3))

        ## scan left tests
        startPoint4 = startPoint2
        q4 = FreeAndSimpleScanner.line_scan_from_coordinate(startPoint4,\
            gameboardDim, usedRegions, direction = "left", increment = "auto")
        print("scan left at {} : {}".format(startPoint4, q4))
        self.assertTrue(q4 == (0.49899999999999956, 1.5), "error: right test start {} : got {}".format(startPoint4, q4))

        ## scan up tests
        startPoint5 = (1,1)
        q5 = FreeAndSimpleScanner.line_scan_from_coordinate(startPoint5,\
            gameboardDim, usedRegions, direction = "up", increment = "auto")
        print("scan up at {} : {}".format(startPoint5, q5))
        self.assertTrue(q5 == False, "error: right test start {} : got {}".format(startPoint5, q5))

        startPoint6 = (2,2)
        q6 = FreeAndSimpleScanner.line_scan_from_coordinate(startPoint6,\
            gameboardDim, usedRegions, direction = "up", increment = "auto")
        print("scan up at {} : {}".format(startPoint6, q6))
        self.assertTrue(q6 == (2,2), "error: right test start {} : got {}".format(startPoint6, q6))

        ## scan down tests
        startPoint7 = startPoint5
        q7 = FreeAndSimpleScanner.line_scan_from_coordinate(startPoint7,\
            gameboardDim, usedRegions, direction = "up", increment = "auto")
        print("scan up at {} : {}".format(startPoint7, q7))
        self.assertTrue(q7 == False, "error: right test start {} : got {}".format(startPoint7, q7))


        startPoint8 = startPoint6
        q8 = FreeAndSimpleScanner.line_scan_from_coordinate(startPoint8,\
            gameboardDim, usedRegions, direction = "down", increment = "auto")
        print("scan up at {} : {}".format(startPoint8, q8))
        self.assertTrue(q8 == (2,2), "error: right test start {} : got {}".format(startPoint8, q8))


    ## TODO : complete tests
    def test_FreeAndSimpleScanner_LineScanFromCoordinateForExtreme(self):
        gameboardDim = (3,3)
        usedRegions = [((0.5,0), (1.5,3)), ((2.9,2.9), (3,3))]

        # test scan
        ## scan right tests
        startPoint1 = (0, 1.5)
        q1,_ = FreeAndSimpleScanner.line_scan_from_coordinate_for_extreme(startPoint1,\
            gameboardDim, usedRegions, direction = "right", increment = "auto")
        ##print("scan right at {} : {}".format(startPoint1, q1))
        startPoint2 = (0.5,1.5)
        q2,_ = FreeAndSimpleScanner.line_scan_from_coordinate_for_extreme(startPoint2,\
            gameboardDim, usedRegions, direction = "right", increment = "auto")
        ##print("scan right at {} : {}".format(startPoint2, q2))
        startPoint3 = (1.50000001,1.5)
        q3,_ = FreeAndSimpleScanner.line_scan_from_coordinate_for_extreme(startPoint3,\
            gameboardDim, usedRegions, direction = "right", increment = "auto")
        ##print("scan right at {} : {}".format(startPoint3, q3))

        self.assertTrue(abs(q1[0] - 0.5) <= 9/1000 and q1[1] == 1.5, "wrong q1")
        self.assertTrue(abs(q2[0] - 1.5) <= 9/1000 and q1[1] == 1.5, "wrong q2")
        self.assertTrue(abs(q3[0] - 3) <= 9/1000 and q1[1] == 1.5, "wrong q3")

    def test_FreeAndSimpleScanner_RightAngleScanFromCoordinate2(self):
        gameboardDim = (3,2)
        ##ur1 = ((0.75,1.25),(1.25,1.75))
        ur2 = ((0,0),(0.5,0.5))
        ##usedRegions = [ur1,ur2]
        usedRegions =[ur2]

        # scan tests
        # point above used
        coord = (0.51,0.51)

        ## left, down
        dx, dy = "left", "down"
        reg = FreeAndSimpleScanner.right_angle_scan_from_coordinate(coord, gameboardDim, usedRegions, dx, dy)
        self.assertTrue(reg == ((0, 0), (0.51, 0.51)), "reg ld wrong {}".format(reg))

        ## left, up
        dx, dy = "left", "up"
        reg = FreeAndSimpleScanner.right_angle_scan_from_coordinate(coord, gameboardDim, usedRegions, dx, dy)
        self.assertTrue(reg == ((0, 0.51), (0.51, 2)), "reg lu wrong {}".format(reg))
        print("reg :\t", reg)


        ## right, down
        dx, dy = "right", "down"
        reg = FreeAndSimpleScanner.right_angle_scan_from_coordinate(coord, gameboardDim, usedRegions, dx, dy)
        print("reg rd :\t",reg)
        self.assertTrue(reg == ((0.51, 0), (3, 0.51)), "reg rd wrong {}".format(reg))

        ## right, up
        dx, dy = "right", "up"
        reg = FreeAndSimpleScanner.right_angle_scan_from_coordinate(coord, gameboardDim, usedRegions, dx, dy)
        ##print("reg ru :\t",reg)
        self.assertTrue(reg == ((0.51, 0.51), (3, 2)), "reg ru wrong {}".format(reg))

        ##### try with coord == (0.5,0.5)
        coord = (0.5,0.5)

        dx, dy = "left", "down"
        reg = FreeAndSimpleScanner.right_angle_scan_from_coordinate(coord, gameboardDim, usedRegions, dx, dy)
        self.assertTrue(reg == ((0.5, 0.5), (0.5, 0.5)), "#2 reg ld wrong {}".format(reg))
        ##print("reg x:\t", reg)


    @staticmethod
    def test_FreeAndSimpleScanner_RightAngleScanFromCoordinate():

        gameboardDim = (3,2)
        ur1 = ((0.75,1.25),(1.25,1.75))
        ur2 = ((0,0),(0.5,0.5))
        usedRegions = [ur1,ur2]

        ##coord = (0.5001,0.5001)
        coord = (1.5,1.5)
        dx, dy = "right", "up"
        reg = FreeAndSimpleScanner.right_angle_scan_from_coordinate(coord, gameboardDim, usedRegions, dx, dy)
        print("reg:\t",reg)
        # assert
        ## ((0.5001, 0.5001), (3, 2))

        dx, dy = "right", "down"
        reg2 = FreeAndSimpleScanner.right_angle_scan_from_coordinate(coord, gameboardDim, usedRegions, dx, dy)
        print("reg2:\t",reg2)

        dx, dy = "left", "up"
        reg3 = FreeAndSimpleScanner.right_angle_scan_from_coordinate(coord, gameboardDim, usedRegions, dx, dy)
        print("reg3:\t",reg3)

        dx, dy = "left", "down"
        reg4 = FreeAndSimpleScanner.right_angle_scan_from_coordinate(coord, gameboardDim, usedRegions, dx, dy)
        print("reg4:\t",reg4)

        coord = (0.5,0.5)
        dx, dy = "right", "up"
        reg = FreeAndSimpleScanner.right_angle_scan_from_coordinate(coord, gameboardDim, usedRegions, dx, dy)

        # assert
        ## ((0.5001, 0.5001), (3, 2))

        dx, dy = "right", "down"
        reg2 = FreeAndSimpleScanner.right_angle_scan_from_coordinate(coord, gameboardDim, usedRegions, dx, dy)
        print("reg2:\t",reg2)


        dx, dy = "left", "up"
        reg3 = FreeAndSimpleScanner.right_angle_scan_from_coordinate(coord, gameboardDim, usedRegions, dx, dy)
        print("reg3:\t",reg3)

        dx, dy = "left", "down"
        reg4 = FreeAndSimpleScanner.right_angle_scan_from_coordinate(coord, gameboardDim, usedRegions, dx, dy)
        print("reg4:\t",reg4)


    @staticmethod
    def is_equal_rounded(t1, t2):

        e = 10 ** (-5)
        d1, d2 = abs(t2[0] - t1[0]), abs(t2[1] - t1[1])

        print("t1 {}\tt2 {}".format(t1,t2))

        if d1 >= e or d2 >= e:
            return False
        return True



#----------------------------------------

def t():
    FreeAndSimpleScannerMethodsTest.test_FreeAndSimpleScanner_LineScanFromCoordinate()
    #FreeAndSimpleScannerMethodsTest.test_FreeAndSimpleScanner_RightAngleScanFromCoordinate()
    #FreeAndSimpleScannerMethodsTest.test_FreeAndSimpleScanner_LineScanFromCoordinate()
    #FreeAndSimpleScannerMethodsTest.test_FreeAndSimpleScanner_LineScanFromCoordinateForExtreme()
    #FreeAndSimpleScannerMethodsTest.test_FreeAndSimpleScanner_RightAngleScanFromCoordinate2()
    return
#----------------------------------------

if __name__ == "__main__":
    unittest.main()
    #t()

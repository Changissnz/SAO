from FreeAndSimpleScanner import *
import unittest

class AreaScannerMethodsTest(unittest.TestCase):

    def test_AreaScanner_GetHorizontalCoexistenceBetweenLinesets(self):
        l11 = ((-2, -2), (2, -2))
        l12 = ((3, -2), (4.5, -2))

        l21 = ((-2,-4), (-1,-4))
        l22 = ((1.5, -4), (2.5, -4))
        l23 = ((2.9,-4), (3.8, -4))
        l24 = ((4.9, -4), (5.5, -4))
        l25 = ((-5, -4), (-2.1, -4))

        ls1 = [l11, l12]
        ls2 = [l21, l22, l23]
        q = AreaScanner.get_horizontal_coexistence_between_linesets(ls1,ls2)
        self.assertTrue(q == [(-2, -1), (1.5, 2), (3, 3.8)])

        ls1 = [l11, l12]
        ls2 = [l21, l22, l23, l24, l25]
        q = AreaScanner.get_horizontal_coexistence_between_linesets(ls1,ls2)
        self.assertTrue(q == [(-2, -1), (1.5, 2), (3, 3.8)])

        ls1 = [l11, l12]
        ls2 = [l21]
        q = AreaScanner.get_horizontal_coexistence_between_linesets(ls1,ls2)
        self.assertTrue(q == [(-2, -1)])

        ls1 = [l11, l12]
        ls2 = [l22]
        q = AreaScanner.get_horizontal_coexistence_between_linesets(ls1,ls2)
        self.assertTrue(q == [(1.5, 2)])

    # TODO : work on this
    ##@staticmethod
    def test_AreaScanner_ScanCollectFreeLineset1(self):#self):
        # test method below
        ##     def scan_collect_free_lineset(startCoord, gameboardDim, usedRegions, direction = "left", mode = "shaded", increment = 10 **(-5)):

        # test 1 case
        startCoord = (0, 1.5)
        gameboardDim = (3,3)
        usedRegions = [((0.5,0), (1.5,3))]
        ls,_ = AreaScanner.scan_collect_free_lineset_(startCoord, gameboardDim, usedRegions)
        actual = [((0, 1.5), (0.4980000000000004, 1.5)), ((1.5029999999999826, 1.5), (2.9970000000000026, 1.5))]
        print("LS:\t", ls)
        self.assertTrue(len(ls) == 2, "invalid length {}".format(len(ls)))
        self.assertAlmostEqual(ls, actual, "wrong output")

    """
    description:
    - tests the methods
    -   AreaScanner.scan_collect_free_lineset_
    -   AreaScanner.get_horizontal_coexistence_between_linesets
    """
    #@staticmethod
    def test_AreaScanner_ScanCollectFreeLineset2(self):
        usedRegions = [((0.5,0.5),(2,2))]
        wr1 = ((0,0),(0.5,0.5))

        # test variable startCoord
        sc1 = (0,1)
        sc2 = (0, 2)
        sc3 = (0, 2.5)
        sc4 = (0, 0.5)
        sc5 = (0, 0.49)

        ls1,_ = AreaScanner.scan_collect_free_lineset_(sc1, wr1, usedRegions)
        ls2,_ = AreaScanner.scan_collect_free_lineset_(sc2, wr1, usedRegions)
        ls3,_ = AreaScanner.scan_collect_free_lineset_(sc3, wr1, usedRegions)
        ls4,_ = AreaScanner.scan_collect_free_lineset_(sc4, wr1, usedRegions)
        ls5,_ = AreaScanner.scan_collect_free_lineset_(sc5, wr1, usedRegions)
        """
        print("*ls 1 :\t", ls1)
        print("*ls 2 :\t", ls2)
        print("*ls 3 :\t", ls3)
        print("*ls 4 :\t", ls4)
        print("*ls 5 :\t", ls5)
        print()
        """

        ## get answers
        a1 = ((0, 1), (0.4995000000000004, 1))
        a2 = ((0, 2), (0.4995000000000004, 2))
        a3 = ((0, 2.5), (0.4995000000000004, 2.5))
        a4 = ((0, 0.5), (0.4995000000000004, 0.5))
        a5 = ((0, 0.49), (0.5, 0.49))

        c2 = lambda x1,x2 : True if AreaScannerMethodsTest.is_equal_tuplepair_rounded(x1[0],x2[0])\
            and AreaScannerMethodsTest.is_equal_tuplepair_rounded(x1[1], x2[1]) else False

        self.assertTrue(c2(a1, ls1[0]), "wrong ls1 {}".format(ls1[0]))
        self.assertTrue(c2(a2, ls2[0]), "wrong ls2 {}".format(ls2[0]))
        self.assertTrue(c2(a3, ls3[0]), "wrong ls3 {}".format(ls3[0]))
        self.assertTrue(c2(a4, ls4[0]), "wrong ls4 {}".format(ls4[0]))
        self.assertTrue(c2(a5, ls5[0]), "wrong ls5 {}".format(ls5[0]))

        wr1 = ((0,0), (3,3))
        ls1,_ = AreaScanner.scan_collect_free_lineset_(sc1, wr1, usedRegions)
        ls2,_ = AreaScanner.scan_collect_free_lineset_(sc2, wr1, usedRegions)
        ls3,_ = AreaScanner.scan_collect_free_lineset_(sc3, wr1, usedRegions)
        ls4,_ = AreaScanner.scan_collect_free_lineset_(sc4, wr1, usedRegions)
        ls5,_ = AreaScanner.scan_collect_free_lineset_(sc5, wr1, usedRegions)

        """
        print("*ls 1 :\t", ls1)
        print("*ls 2 :\t", ls2)
        print("*ls 3 :\t", ls3)
        print("*ls 4 :\t", ls4)
        print("*ls 5 :\t", ls5)
        """

        q1 = [((0, 1), (0.4980000000000004, 1)), ((2.000999999999965, 1), (2.9970000000000026, 1))]
        q2 = [((0, 2), (0.4980000000000004, 2)), ((2.000999999999965, 2), (2.9970000000000026, 2))]
        q3 = [((0, 2.5), (2.9970000000000026, 2.5))]
        q4 = [((0, 0.5), (0.4980000000000004, 0.5)), ((2.000999999999965, 0.5), (2.9970000000000026, 0.5))]
        q5 = [((0, 0.49), (2.9970000000000026, 0.49))]

        self.assertAlmostEqual(q1,\
            ls1, places = 1, msg = "wrong ls1")
        self.assertAlmostEqual(q2, ls2, places = 1, msg = "wrong ls2")
        self.assertAlmostEqual(q3, ls3, places = 1, msg = "wrong ls3 {}".format(ls3))
        self.assertAlmostEqual(q4, ls4, places = 1, msg = "wrong ls4")
        self.assertAlmostEqual(q5,ls5, places = 1, msg = "wrong ls5")

    #@staticmethod
    def test_AreaScanner_ScanCollectFreeLineset3(self):
        gameboardDim = (3,3)
        usedRegions = [((0.5,0.5),(2,2))]
        wr1 = ((0,0),(0.5,0.5))

        coord = (0,0.5)
        ls1 = AreaScanner.scan_collect_free_lineset(coord, gameboardDim, usedRegions, direction = "right", increment = 10 **(-2))
        #print("lineset :\t",ls1)
        qls1 = [((0, 0.5), (0.4980000000000004, 0.5)), ((2.000999999999965, 0.5), (2.9970000000000026, 0.5))]

        self.assertAlmostEqual(qls1, ls1)

        coord = (1,0.5)
        ls2 = AreaScanner.scan_collect_free_lineset(coord, gameboardDim, usedRegions, direction = "right", increment = 10 **(-2))
        print("lineset 2:\t",ls2)
        qls2 = [((2.001999999999964, 0.5), (2.9950000000000014, 0.5))]
        self.assertAlmostEqual(qls2, ls2)


    ## TODO : finish this
    #@staticmethod
    def test_AreaScanner_SloppyAreaScan(self):

        usedRegions = [((0.5,0.5),(2,2))]
        usedRegions = []
        wr1 = ((0,0),(0.5,0.5))
        ##wr1 = ((0,0), (0.5,3))
        wr2 = ((0,0.5),(2,2))
        wr3 = ((0.5,0.5),(3,3))
        wr4 = ((2.0,0.5),(2.1,3))

        # check coordinate limits
        a1 = AreaScanner.sloppy_area_scan(wr1, usedRegions)
        a2 = AreaScanner.sloppy_area_scan(wr2, usedRegions)
        a3 = AreaScanner.sloppy_area_scan(wr3, usedRegions)
        a4 = AreaScanner.sloppy_area_scan(wr4, usedRegions)

        self.assertAlmostEqual(a1, 0.24500000000000013, 1)
        self.assertAlmostEqual(a2, 2.980000000000002, 1)
        self.assertAlmostEqual(a3, 6.250000000000021, 1)
        self.assertAlmostEqual(a4, 0.2500000000000002, 1)

        """
        print("region {} :\tarea {}".format(wr1,a1))
        print("region {} :\tarea {}".format(wr2,a2))
        print("region {} :\tarea {}".format(wr3,a3))
        print("region {} :\tarea {}".format(wr4,a4))
        """

    #@staticmethod
    def test_AreaScanner_GetBestRegionGivenCoordinates(self):

        gameboardDim = (3,2)
        ##ur1 = ((0.75,1.25),(1.25,1.75))
        ur2 = ((0,0),(0.5,0.5))
        usedRegions = [ur2]
        coord = (0.51,0.51)

        q,_ = AreaScanner.get_best_region_given_coordinates(coord, gameboardDim, usedRegions, increment = 10**(-2))
        print("q1:\n",q)
        self.assertTrue(AreaScannerMethodsTest.are_equal_regions(q, ((0.5, 0.5), (3, 2))))

        coord = (2,2)
        q,_ = AreaScanner.get_best_region_given_coordinates(coord, gameboardDim, usedRegions, increment = 10**(-2))
        print("q2:\n",q)
        self.assertTrue(AreaScannerMethodsTest.are_equal_regions(q,\
            ((0.002000000000035229, 0.002000000000035229), (2, 2))))

        ## test bottom right corner
        coord = (2,0)
        q,_ = AreaScanner.get_best_region_given_coordinates(coord, gameboardDim, usedRegions, increment = 10**(-2))
        print("q3:\n",q)
        self.assertTrue(AreaScannerMethodsTest.are_equal_regions(q, ((0.59, 0), (2, 2)))) #? TODO

        coord = (0,0)
        q = AreaScanner.get_best_region_given_coordinates(coord, gameboardDim, usedRegions, increment = 10**(-2))
        self.assertTrue(False == q, "incorrect q3 : {}".format(q))

    @staticmethod
    def test_AreaScanner_GetBestRegionGivenCoordinates2():

        gameboardDim = (3,2)
        ##ur1 = ((0.75,1.25),(1.25,1.75))
        ur2 = ((0,0),(0.5,0.5))
        usedRegions = [ur2]
        coord = (0.51,0.51)

        q = AreaScanner.get_best_region_given_coordinates(coord, gameboardDim, usedRegions, increment = 10**(-2))
        print("Q1 :\t", q)

    ##@staticmethod
    def test_AreaScanner_GetBestRegionFitGivenWantedDimensions(self):
        ##def get_best_region_fit_given_wanted_dimensions(coord, gameboardDim, wantedDimensions, usedRegions, increment = 10**(-2)):
        gameboardDim = (3,3)
        ur2 = ((0,0),(1,1))
        ur = [ur2]

        wantedDimensions = (1,1)
        c1 = (1.01,1.01)
        r, a = AreaScanner.get_best_region_fit_given_wanted_dimensions(c1, gameboardDim, wantedDimensions, ur)
        print("region for {} of {} :\n{}".format(c1, wantedDimensions, r))
        #self.assertAlmostEqual(((0.010000000000000009, 1.01), (1.01, 2.01099999999989)), r)

        wantedDimensions = (2.5,2.5)
        c1 = (1.01,1.01)
        r, _ = AreaScanner.get_best_region_fit_given_wanted_dimensions(c1, gameboardDim, wantedDimensions, ur)
        print("region for {} of {} :\n{}".format(c1, wantedDimensions, r))
        #self.assertAlmostEqual(((1.01, 1.01), (3, 3)), r)

        wantedDimensions = (1.5,1.5)
        c1 = (1.01,1.01)
        r, _ = AreaScanner.get_best_region_fit_given_wanted_dimensions(c1, gameboardDim, wantedDimensions, ur)
        print("region for {} of {} :\n{}".format(c1, wantedDimensions, r))
        #self.assertAlmostEqual(((1.01, 1.01), (2.51, 2.5100000000000566)), r)

        return -1

    """
    """
    @staticmethod
    def test_AreaScanner_GetBestRegionGivenWantedDimensions_SquareFit():

        gameboardDim = (3,3)
        ur2 = ((0,0),(1,1))
        ur = [ur2]

        coord = (1.01,1.01)
        wantedDimensions = (2,2)
        calibrateMode = "square"

        q = AreaScanner.get_best_region_fit_given_wanted_dimensions(coord, gameboardDim,\
            wantedDimensions, ur, increment = 10**(-2), calibrateMode = calibrateMode)
        print("HERE:\t", q)
        #self.assertAlmostEqual(q[0], ((1.01, 1.01), (3.0, 3)))

        coord = (3,3)
        wantedDimensions = (3,3)
        q = AreaScanner.get_best_region_fit_given_wanted_dimensions(coord, gameboardDim,\
            wantedDimensions, ur, increment = 10**(-2), calibrateMode = calibrateMode)
        print("HERE2:\t", q)
        #self.assertAlmostEqual(q[0], ((0, 0), (3, 3)))

    @staticmethod
    def test_AreaScanner_GetBestRegionGivenWantedDimensions_SquareFit2():
        coord = (0,0)
        wantedDimensions = (2,2)
        gameboardDim = (8,8)
        ur = []
        calibrateMode = "square"

        q = AreaScanner.get_best_region_fit_given_wanted_dimensions(coord, gameboardDim,\
            wantedDimensions, ur, increment = 10**(-2), calibrateMode = calibrateMode)
        print("HERE2:\t", q)



    # TODO : refactor below 2 duplicate methods
    '''
    description:
    - for tuples
    '''
    @staticmethod
    def is_equal_tuplepair_rounded(t1, t2, e = 1):

        ##d1, d2 = abs(t2[0] - t1[0]), abs(t2[1] - t1[1])
        d1, d2 =  abs(round(t2[0], e) - round(t1[0], e)),\
            abs(round(t2[1], e) - round(t1[1], e))
        ##print("t1 {}\tt2 {}".format(t1,t2))

        if d1 != 0 or d2 != 0:
            return False
        return True

    @staticmethod
    def are_equal_regions(r1, r2):

        if AreaScannerMethodsTest.is_equal_tuplepair_rounded(r1[0], r2[0])\
            and AreaScannerMethodsTest.is_equal_tuplepair_rounded(r1[1],r2[1]):
            return True
        return False

def t():
    #AreaScannerMethodsTest.test_AreaScanner_SloppyAreaScan()
    #AreaScannerMethodsTest.test_AreaScanner_ScanCollectFreeLineset2()#self):
    #AreaScannerMethodsTest.test_AreaScanner_ScanCollectFreeLineset3()#self):
    #AreaScannerMethodsTest.test_AreaScanner_t2()
    #AreaScannerMethodsTest.h()
    #AreaScannerMethodsTest.test_AreaScanner_SloppyAreaScan2()
    #AreaScannerMethodsTest.test_AreaScanner_GetBestRegionGivenCoordinates()
    #AreaScannerMethodsTest.test_AreaScanner_GetBestRegionGivenCoordinates2()
    #AreaScannerMethodsTest.test_AreaScanner_GetBestRegionFitGivenWantedDimensions()
    #AreaScannerMethodsTest.test_AreaScanner_GetBestRegionGivenWantedDimensions_SquareFit2()
    return

if __name__ == "__main__":
    #t()
    unittest.main()

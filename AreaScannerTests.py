from AreaScanner import *
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
        actual = [((0, 1.5), (0.4980000000000004, 1.5)), ((1.5029999999999826, 1.5), (3, 1.5))]

        self.assertTrue(len(ls) == 2, "invalid length {}".format(len(ls)))
        self.assertTrue(ls == actual, "wrong output")

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
        print("*ls 1 :\t", ls1)
        print("*ls 2 :\t", ls2)
        print("*ls 3 :\t", ls3)
        print("*ls 4 :\t", ls4)
        print("*ls 5 :\t", ls5)
        print()
        self.assertTrue([((0, 1), (0.4995000000000004, 1))] == ls1, "wrong ls1")
        self.assertTrue([((0, 2), (0.4995000000000004, 2))] == ls2, "wrong ls2")
        self.assertTrue([((0, 2.5), (0.4995000000000004, 2.5))] == ls3, "wrong ls3")
        self.assertTrue([((0, 0.5), (0.4995000000000004, 0.5))] == ls4, "wrong ls4")
        self.assertTrue([((0, 0.49), (0.5, 0.49))] == ls5, "wrong ls5")

        wr1 = ((0,0), (3,3))
        ls1,_ = AreaScanner.scan_collect_free_lineset_(sc1, wr1, usedRegions)
        ls2,_ = AreaScanner.scan_collect_free_lineset_(sc2, wr1, usedRegions)
        ls3,_ = AreaScanner.scan_collect_free_lineset_(sc3, wr1, usedRegions)
        ls4,_ = AreaScanner.scan_collect_free_lineset_(sc4, wr1, usedRegions)
        ls5,_ = AreaScanner.scan_collect_free_lineset_(sc5, wr1, usedRegions)

        print("*ls 1 :\t", ls1)
        print("*ls 2 :\t", ls2)
        print("*ls 3 :\t", ls3)
        print("*ls 4 :\t", ls4)
        print("*ls 5 :\t", ls5)
        self.assertTrue([((0, 1), (0.4980000000000004, 1)),\
            ((2.000999999999965, 1), (3, 1))] == ls1, "wrong ls1")
        self.assertTrue([((0, 2), (0.4980000000000004, 2)), \
            ((2.000999999999965, 2), (3, 2))] == ls2, "wrong ls2")
        self.assertTrue([((0, 2.5), (0.4980000000000004, 2.5)),\
            ((2.000999999999965, 2.5), (3, 2.5))] == ls3, "wrong ls3")
        self.assertTrue([((0, 0.5), (0.4980000000000004, 0.5)),\
            ((2.000999999999965, 0.5), (3, 0.5))] == ls4, "wrong ls4")
        self.assertTrue([((0, 0.49), (3, 0.49))] == ls5, "wrong ls5")

    @staticmethod
    def test_AreaScanner_ScanCollectFreeLineset3():
        gameboardDim = (3,3)
        usedRegions = [((0.5,0.5),(2,2))]
        wr1 = ((0,0),(0.5,0.5))

        coord = (0,0.5)
        ls1 = AreaScanner.scan_collect_free_lineset(coord, gameboardDim, usedRegions, direction = "right", increment = 10 **(-2))
        print("lineset :\t",ls1)
        qls1 = [((0, 0.5), (0.4980000000000004, 0.5)), ((2.000999999999965, 0.5), (3, 0.5))]

        coord = (1,0.5)
        ls2 = AreaScanner.scan_collect_free_lineset(coord, gameboardDim, usedRegions, direction = "right", increment = 10 **(-2))
        print("lineset 2:\t",ls2)
        qls2 = [((2.001999999999964, 0.5), (3, 0.5))]

    # DELETE
    """
    @staticmethod
    def h():
        usedRegions = [((0.5,0.5),(2,2))]

        wr3 = ((1.5,0.5),(2,3))
        sc1 = wr3[0]
        sc1 = (1.6, 2.5)
        ##ls1 = AreaScanner.scan_collect_free_lineset(sc1, wr3, usedRegions)
        ##print("\n\nXXXX ls1 :\t",ls1)
        ls, coord = AreaScanner.scan_collect_free_lineset_(sc1, wr3, usedRegions)

        print("LS\t",ls)
        print("COORD\t",coord)

        # check coordinate limits
        ##a3 = AreaScanner.sloppy_area_scan(wr3, usedRegions)
    """

    ## TODO : finish this
    @staticmethod
    def test_AreaScanner_SloppyAreaScan():

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

        print("region {} :\tarea {}".format(wr1,a1))
        print("region {} :\tarea {}".format(wr2,a2))
        print("region {} :\tarea {}".format(wr3,a3))
        print("region {} :\tarea {}".format(wr4,a4))

        ## assert below
        """
area 0.24500000000000013
region ((0, 0.5), (2, 2)) :	area 2.980000000000002
region ((0.5, 0.5), (3, 3)) :	area 6.250000000000021
region ((2.0, 0.5), (2.1, 3)) :	area 0.2500000000000002
        """

    """
    @staticmethod
    def test_AreaScanner_GetBestRegionGivenCoordinates():
##     def get_best_region_given_coordinates(coord, gameboardDim, usedRegions, increment = 10**(-2)):
        gameboardDim = (3,2)
        ur1 = ((0.75,1.25),(1.25,1.75))
        ur2 = ((0,0),(0.5,0.5))
        usedRegions = [ur1,ur2]

        coord = (0.5001,0.5001)

        ## right-angle scans for each
        lu = FreeAndSimpleScanner.right_angle_scan_from_coordinate(coord, gameboardDim, usedRegions, "left", "up")
        ld = FreeAndSimpleScanner.right_angle_scan_from_coordinate(coord, gameboardDim, usedRegions, "left", "down")
        ru = FreeAndSimpleScanner.right_angle_scan_from_coordinate(coord, gameboardDim, usedRegions, "right", "up")
        rd = FreeAndSimpleScanner.right_angle_scan_from_coordinate(coord, gameboardDim, usedRegions, "right", "down")
        print("LU:\t", lu)
        print("LD:\t", ld)
        print("RU:\t", ru)
        print("RD:\t", rd)

        # get areas for each


        #print("COORD:\t", AreaScanner.get_best_region_given_coordinates(coord, gameboardDim, usedRegions))



        # try area-scanning

        as1 = AreaScanner.sloppy_area_scan(lu, usedRegions)
        print("lu area:\t", as1)


        as1 = AreaScanner.sloppy_area_scan(ld, usedRegions)
        print("ld area:\t", as1)


        #print("ru:\t", ru)

        ##r1 = AreaScanner.get_best_region_given_coordinates(coord, gameboardDim, usedRegions, increment = 10**(-1))
        ##print("r1 :\t{}".format(r1))


        c2 = (0,1.25001)
        r2 = AreaScanner.get_best_region_given_coordinates(c2, gameboardDim, ur, increment = 10**(-2))
        print("r2 :\t{}".format(r2))

    """


    ## TODO : make assertions for below
    """
    @staticmethod
    def test_AreaScanner_SloppyAreaScan2():
        gameboardDim = (3,2)
        ##ur1 = ((0.75,1.25),(1.25,1.75))
        ur2 = ((0,0),(0.5,0.5))
        ##usedRegions = [ur1,ur2]
        usedRegions = [ur2]

        wantedRegion = ((0,0), (0.5,0.5))
        q = AreaScanner.sloppy_area_scan(wantedRegion, usedRegions, increment = 10**(-2))
        print("q :\t",q)

        wantedRegion = ((0,0), (0.6,0.6))
        q = AreaScanner.sloppy_area_scan(wantedRegion, usedRegions, increment = 10**(-2))
        print("q :\t",q)

        wantedRegion = ((0,0), (3,2))
        q = AreaScanner.sloppy_area_scan(wantedRegion, usedRegions, increment = 10**(-2))
        print("q :\t",q)


        usedRegions = [ur2, ((2,1), (3,2))]
        wantedRegion = ((0,0), (3,2))
        q = AreaScanner.sloppy_area_scan(wantedRegion, usedRegions, increment = 10**(-2))
        print("q :\t",q)
    """

    @staticmethod
    def test_AreaScanner_GetBestRegionGivenCoordinates():

        gameboardDim = (3,2)
        ##ur1 = ((0.75,1.25),(1.25,1.75))
        ur2 = ((0,0),(0.5,0.5))
        usedRegions = [ur2]
        coord = (0.51,0.51)

        q,_ = AreaScanner.get_best_region_given_coordinates(coord, gameboardDim, usedRegions, increment = 10**(-2))
        print("q1:\n",q)

        coord = (2,2)
        q,_ = AreaScanner.get_best_region_given_coordinates(coord, gameboardDim, usedRegions, increment = 10**(-2))
        print("q2:\n",q)




def t():
    #AreaScannerMethodsTest.test_AreaScanner_SloppyAreaScan()
    #AreaScannerMethodsTest.test_AreaScanner_ScanCollectFreeLineset2()#self):
    #AreaScannerMethodsTest.test_AreaScanner_ScanCollectFreeLineset3()#self):
    #AreaScannerMethodsTest.test_AreaScanner_t2()
    #AreaScannerMethodsTest.h()
    #AreaScannerMethodsTest.test_AreaScanner_SloppyAreaScan2()
    AreaScannerMethodsTest.test_AreaScanner_GetBestRegionGivenCoordinates()
    return

if __name__ == "__main__":
    t()
    #unittest.main()

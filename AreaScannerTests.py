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

        wr1 = ((0,0),(0.5,0.5))
        ##wr1 = ((0,0), (0.5,3))
        #wr2 = ((0,0.5),(2,2))
        wr3 = ((0.5,0.5),(3,3))
        #wr4 = ((2.0,0.5),(2,3))

        # check coordinate limits
        #a1 = AreaScanner.sloppy_area_scan(wr1, usedRegions)
        #a2 = AreaScanner.sloppy_area_scan(wr2, usedRegions)
        a3 = AreaScanner.sloppy_area_scan(wr3, usedRegions)
        #a4 = AreaScanner.sloppy_area_scan(wr4, usedRegions)

        #print("region {} :\tarea {}".format(wr1,a1))
        #print("region {} :\tarea {}".format(wr2,a2))
        print("region {} :\tarea {}".format(wr3,a3))
        #print("region {} :\tarea {}".format(wr4,a4))


def t():
    AreaScannerMethodsTest.test_AreaScanner_SloppyAreaScan()
    #AreaScannerMethodsTest.test_AreaScanner_ScanCollectFreeLineset2()#self):
    #AreaScannerMethodsTest.test_AreaScanner_t2()
    #AreaScannerMethodsTest.h()
    return

if __name__ == "__main__":
    #t()
    unittest.main()

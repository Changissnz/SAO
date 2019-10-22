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

    def test_FreeAndSimpleScanner_LineScanFromCoordinate(self):
    ##def line_scan_from_coordinate(coord, gameboardDim, usedRegions, direction = "left", increment = "auto"):

        return -1


    def test_FreeAndSimpleScanner_RightAngleScanFromCoordinate(self):
        return -1




    @staticmethod
    def is_equal_rounded(t1, t2):

        e = 10 ** (-5)
        d1, d2 = abs(t2[0] - t1[0]), abs(t2[1] - t1[1])

        print("t1 {}\tt2 {}".format(t1,t2))

        if d1 >= e or d2 >= e:
            return False
        return True

if __name__ == "__main__":
    unittest.main()

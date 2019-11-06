'''
this file contains time tests for scanner algorithms
'''

from FreeAndSimpleScanner import *
import unittest
from time import time
from random import uniform

class AreaScannerMethodsTest(unittest.TestCase):

    @staticmethod
    def used_regions_sample():

        usedRegions = [((5.5, 1), (7.5, 4)), ((1, 5.5), (3.5, 7.5))]
        return usedRegions


    @staticmethod
    def test_AreaScanner_scan_n_objects_for_time(n = 20):
        ur = AreaScannerMethodsTest.used_regions_sample()
        gameboardDim = (8,8)

        t = time()
        for i in range(n):

            # get random region for dim (8,8)
            wr = FreeAndSimpleScanner.random_region_in_dimensions(gameboardDim)
            a = AreaScanner.sloppy_area_scan_mp(ur, 0.1, wr)
            print("AREA :\t", a)

        rt = time() - t
        print("runtime for scanning {} objects :\t{}".format(n, rt))


if __name__ == "__main__":
    #t()
    unittest.main()
